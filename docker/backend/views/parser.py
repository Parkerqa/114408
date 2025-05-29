import io
import os
import re
import tempfile

import opencc
from core.upload_utils import is_valid_image
from model.parser_model import save_result
from paddleocr import PaddleOCR
from pyzbar.pyzbar import decode
from PIL import Image

# 初始化模型
ocr_model = PaddleOCR(lang='ch', use_gpu=False)

# 初始化語言轉換器
converter = opencc.OpenCC('s2t')

async def snn_logic(image):
    img_bytes = await image.read()
    # 格式檢查
    is_valid, reason = is_valid_image(image, img_bytes)
    if not is_valid:
        return reason, "error", 400, None
    try:
        print("snn running")
        return 0, "success", 200, img_bytes
    except Exception as e:
        print(e)
        return "SNN 分類錯誤", "error", 500, None

async def ocr_logic(image, snn_result: int):
    try:
        # 建立暫存圖片檔案
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(image)
            img_path = tmp.name

        try:
            # 執行 OCR
            ocr_result = ocr_model.ocr(img_path)

        except Exception as e:
            print(e)
            return "OCR 辨識錯誤", "error", 500, None

        finally:
            os.remove(img_path)

        extracted_info = {
            "TID": None,
            "No": None,
            "time": None,
            "title": "test",
            "money": None
        }

        for item in ocr_result[0]:
            try:
                coordinates, (text, confidence) = item
                text = converter.convert(text)

                if re.match(r"[A-Z]{2}\d{8}", text):
                    extracted_info["TID"] = text

                elif "統一編號：" in text or re.match(r"\d{8}", text):
                    match = re.search(r"\d{8}", text)
                    if match:
                        extracted_info["No"] = match.group()

                elif re.match(r"\d{4}/\d{2}/\d{2}\d{2}:\d{2}:\d{2}", text):
                    fixed_date = text[:10].replace("/", "-") + " " + text[10:]
                    extracted_info["time"] = fixed_date

                elif "現金費" in text:
                    amount = re.search(r"\d+", text)
                    if amount:
                        extracted_info["money"] = amount.group()
            except Exception as line_err:
                # 記錄錯誤，但繼續處理其他
                print(f"OCR 行處理錯誤：{line_err}")

        # save ocr result
        if save_result(extracted_info):
            return "已存入資料庫", "success", 200

        return "資料儲存失敗", "error", 500

    except Exception as e:
        print(e)
        return "伺服器錯誤", "error", 500

def extract_qrcodes(image):
    img = Image.open(io.BytesIO(image))
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
        result['error'] = f'解析品項時錯誤: {e}'
    return result

def qrcode_decoder_logic(image, snn_result: int):
    left_data, right_data = extract_qrcodes(image)
    result = parse_invoice_qrcodes(left_data, right_data)
    for key, value in result.items():
        print(f"{key}: {value}")