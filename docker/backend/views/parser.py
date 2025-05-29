import os
import re
import tempfile

import opencc
from core.upload_utils import is_valid_image
from model.parser_model import save_result
from paddleocr import PaddleOCR

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

async def qrcode_decoder_logic(image):
    img = Image.open(image_path)
    qrcodes = decode(img)
    return [qr.data.decode('utf-8') for qr in qrcodes]