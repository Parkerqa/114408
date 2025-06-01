import io
import re

import opencc
from paddleocr import PaddleOCR
from pyzbar.pyzbar import decode
from PIL import Image
from core.upload_utils import BASE_DIR, INVOICE_UPLOAD_FOLDER
from model.parser_model import save_error, save_qrcode_result, save_ocr_result

from keras.models import load_model
import numpy as np

# 初始化模型
ocr_model = PaddleOCR(lang='ch', use_angle_cls=True, use_gpu=False)

# 初始化語言轉換器
converter = opencc.OpenCC('s2t')

async def snn_logic(image_path) -> int:
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
            quantity = int(items_raw[i+1])
            price = int(items_raw[i+2])
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

async def qrcode_decoder_logic(image_path, ticket_id, invoice_type):
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

async def ocr_logic(image_path, ticket_id, invoice_type):
    try:
        # 執行 OCR
        ocr_result = ocr_model.ocr(str(image_path))
    except Exception as e:
        print(e)
        save_error(ticket_id)
        return

    extracted_info = {
        "invoice_number": None,
        "No": None,
        "date": None,
        "title": None,
        "total_money": None
    }

    for item in ocr_result[0]:
        try:
            coordinates, (text, confidence) = item
            text = converter.convert(text)

            if re.match(r"[A-Z]{2}\d{8}", text):
                extracted_info["invoice_number"] = text

            elif "統一編號：" in text or re.match(r"\d{8}", text):
                match = re.search(r"\d{8}", text)
                if match:
                    extracted_info["No"] = match.group()


            elif re.match(r"\d{4}/\d{2}/\d{2}\d{2}:\d{2}:\d{2}", text):
                try:
                    raw_date = text[:10]  # yyyy/mm/dd
                    raw_time = text[10:]  # hh:mm:ss
                    year, month, day = raw_date.split("/")
                    # 嘗試修正錯誤的 8 → 0
                    year = int(year)
                    month = int(month)
                    day = int(day)

                    if year > 2100:
                        year = int(str(year).replace("8", "0"))

                    if month == 0 or month > 12:
                        month = int(str(month).replace("8", "0"))
                        if month == 0:
                            month = 8

                    if day == 0 or day > 31:
                        day = int(str(day).replace("8", "0"))

                    if month == 0 or month > 12:
                        month = 1

                    if day == 0 or day > 31:
                        day = 1

                    fixed_date = f"{year:04d}-{month:02d}-{day:02d} {raw_time}"
                    extracted_info["date"] = fixed_date
                except Exception as err:
                    print(f"[錯誤] 日期修正失敗: {text} -> {err}")

            elif "費用" in text:
                text = text.replace("：", ":")  # 處理全形冒號
                title = text.split(":")[0] if ":" in text else text
                extracted_info["title"] = title.strip()

            elif "現金費" in text:
                amount_match = re.search(r"\d+", text)
                if amount_match:
                    raw_amount = amount_match.group()
                    # 嘗試修正錯誤的 8 → 0
                    fixed_amount = re.sub(r"8", "0", raw_amount)
                    extracted_info["total_money"] = fixed_amount
        except Exception as line_err:
            # 記錄錯誤，但繼續處理其他
            print(f"OCR 行處理錯誤：{line_err}")

    # save ocr result
    if save_ocr_result(ticket_id, invoice_type, extracted_info):
        return

    save_error(ticket_id)
    return

async def invoice_parser(filename, ticket_id):
    try:
        image_path = BASE_DIR / INVOICE_UPLOAD_FOLDER / filename  # /app/static/invoice/filename

        # 執行 SNN 處理
        invoice_type = await snn_logic(image_path)

        if invoice_type == 0:
            save_error(ticket_id)
        elif invoice_type == 3:
            # 執行 QRCode 解析（電子發票）
            await qrcode_decoder_logic(image_path, ticket_id, invoice_type)
        else:
            # 執行 OCR 處理
            await ocr_logic(image_path, ticket_id, invoice_type)
        return
    except Exception as e:
        save_error(ticket_id)
        print(e)
        return