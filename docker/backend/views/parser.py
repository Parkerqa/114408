import io
import json
import re

import numpy as np
import opencc
from core.upload_utils import BASE_DIR, INVOICE_UPLOAD_FOLDER
from keras.models import load_model
from model.parser_model import save_error, save_ocr_result, save_qrcode_result
from paddleocr import PaddleOCR
from PIL import Image
from pyzbar.pyzbar import decode
from views.openai import ocr_correction_logic

# 初始化模型
ocr_model = PaddleOCR(lang='ch', use_angle_cls=True, use_gpu=False)

# 初始化語言轉換器
converter = opencc.OpenCC('s2t')


def snn_logic(image_path) -> int:
    try:
        # 路徑
        model_path = BASE_DIR / "invoice_single_classifier_siamese.keras"

        # 載入模型
        model = load_model(model_path)

        # 處理圖片
        img = Image.open(image_path).convert("RGB")
        img = img.resize((128, 128))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # 預測
        pred = model.predict(img_array)
        score = float(pred[0][0])

        # 根據預測分數判斷類別
        if score > 0.5:
            return 2  # 傳統發票
        else:
            return 3  # 電子發票
    except Exception as e:
        print(e)
        return 0


def extract_qrcodes(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    img = Image.open(io.BytesIO(image_bytes))
    qrcodes = decode(img)
    if len(qrcodes) != 2:
        raise ValueError("QRCode 數量錯誤")
    sorted_qrcodes = sorted(qrcodes, key=lambda q: q.rect.left)
    return [qr.data.decode('utf-8') for qr in sorted_qrcodes]


def convert_date(tw_date: str) -> str:
    year = int(tw_date[:3]) + 1911
    month = tw_date[3:5]
    day = tw_date[5:7]
    return f"{year}/{month}/{day}"


def decode_item_name(name, encoding):
    try:
        if encoding == '0':
            return name.encode('latin1').decode('big5')
        elif encoding == '2':
            return base64.b64decode(name).decode('utf-8')
        return name
    except Exception as e:
        print(e)
        raise ValueError(f"錯誤的編碼設定:{name}")


def parse_invoice_qrcodes(left_data, right_data):
    result = {
        'invoice_number': left_data[0:10],
        'date': left_data[10:17],
        # '隨機碼': left_data[17:21],
        # '銷售額': left_data[21:29],
        # '總計額': left_data[29:37],
        # '買方統一編號': left_data[37:45],
        # '賣方統一編號': left_data[45:53],
    }

    remaining = left_data[77:] + right_data[2:]
    fields = remaining.split(':')
    del fields[0]

    try:
        # result.update({
        #     '營業人自行使用區': fields[0],
        #     '二維條碼記載完整品目筆數': int(fields[1]),
        #     '該張發票交易品目總筆數': int(fields[2]),
        #     'encoding': fields[3],
        # })
        encoding = fields[3]
        items_raw = fields[4:]
        items = []
        for i in range(0, len(items_raw), 3):
            if i + 2 >= len(items_raw): break
            name = decode_item_name(items_raw[i], encoding)
            quantity = int(items_raw[i + 1])
            price = int(items_raw[i + 2])
            items.append({
                'title': name,
                # '數量': quantity,
                'money': price
            })
        result['items'] = items
    except Exception as e:
        result['items'] = []
        raise Exception("明細解析錯誤")
    return result


def qrcode_decoder_logic(image_path, ticket_id, invoice_type):
    try:
        # 解析 QRCode
        left_data, right_data = extract_qrcodes(image_path)
        result = parse_invoice_qrcodes(left_data, right_data)

        invoice_number = result.get("invoice_number")
        raw_date = result.get("date")
        items = result.get("items", [])

        # 轉換民國 → 西元
        if re.match(r"\d{7}", raw_date):
            year = int(raw_date[:3]) + 1911
            month = raw_date[3:5]
            day = raw_date[5:]
            formatted_date = f"{year}-{month}-{day}"
        else:
            formatted_date = None

        if save_qrcode_result(
                ticket_id,
                invoice_type,
                {
                    "invoice_number": invoice_number,
                    "date": formatted_date,
                    "total_money": sum(item["money"] for item in items)
                },
                items
        ):
            return

        save_error(ticket_id)
    except Exception as e:
        print(e)
        save_error(ticket_id)
        return


def extract_clean_json(content: str) -> str:
    match = re.search(r"\{[\s\S]*?\}", content)
    if match:
        return match.group(0)
    return content


def ocr_logic(image_path, ticket_id, invoice_type):
    try:
        # 步驟 1：執行 OCR，得到原始文字塊
        ocr_result = ocr_model.ocr(str(image_path))
    except Exception as e:
        print(f"[OCR 錯誤] ticket_id={ticket_id}：{e}")
        save_error(ticket_id)
        return

    # 步驟 2：將原始 ocr 結果傳給 ChatGPT 校正與結構化
    try:
        # 整理純文字內容
        text_lines = []
        for item in ocr_result[0]:
            _, (text, _) = item
            text_lines.append(converter.convert(text).strip())

        raw_ocr_text = "\n".join(text_lines)

        prompt = f"""
        請從以下發票文字中擷取欄位，回傳 JSON 格式（五個欄位皆需輸出）：

        - invoice_number（string）：格式為 2 英文字母 + 8 數字
        - date（string）：YYYY-MM-DD，支援 YYYY/MM/DD，若年月日不合理（如 2821/88/31）請修正為合理日期
        - title（string[]）：商品名稱，無明細輸出 []
        - money（number[]）：商品金額，與 title 順序對應，無明細輸出 []
        - total_money（number）：總金額，純數字

        規則：
        - 「單價×數量」格式（如 237×2）請計算總金額
        - 金額若含 TX、Tx、tx，請去除後取數字
        - 商品與金額可能換行，請正確對應

        發票內容如下：

        {raw_ocr_text}
        """

        gpt_response_str = ocr_correction_logic(prompt)
        if not gpt_response_str:
            raise ValueError("GPT 回傳為空")

        cleaned_json_str = extract_clean_json(gpt_response_str)
        structured_data = json.loads(cleaned_json_str)

    except Exception as e:
        print(f"[ChatGPT 校正失敗] ticket_id={ticket_id}：{e}")
        save_error(ticket_id)
        return

    if structured_data.get("title") and structured_data.get("money"):
        if save_ocr_result(ticket_id, invoice_type, structured_data):
            return
    else:
        print(f"[警告] 校正後仍無有效明細，ticket_id={ticket_id}")

    save_error(ticket_id)


def invoice_parser(filename, ticket_id):
    try:
        image_path = BASE_DIR / INVOICE_UPLOAD_FOLDER / filename  # /app/static/invoice/filename

        # 執行 SNN 處理
        invoice_type = snn_logic(image_path)

        if invoice_type == 0:
            save_error(ticket_id)
        elif invoice_type == 3:
            # 執行 QRCode 解析（電子發票）
            qrcode_decoder_logic(image_path, ticket_id, invoice_type)
        else:
            # 執行 OCR 處理
            ocr_logic(image_path, ticket_id, invoice_type)
        return
    except Exception as e:
        save_error(ticket_id)
        print(e)
        return
