import os
import re
import tempfile
from typing import Optional

import opencc
from paddleocr import PaddleOCR


def run_ocr(img_bytes: bytes) -> list:
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp.write(img_bytes)
        img_path = tmp.name

    # Setup model
    ocr_model = PaddleOCR(lang='ch', use_gpu=False)

    # Run the ocr method on the ocr model
    result = ocr_model.ocr(img_path)

    os.remove(tmp.name)

    return result

def extract_invoice_info(ocr_data) -> dict[str, Optional[str]]:
    converter = opencc.OpenCC('s2t')

    extracted_info = {
        "TID": None,
        "No": None,
        "time": None,
        "title": "test",
        "money": None
    }

    for item in ocr_data[0]:
        coordinates, (text, confidence) = item

        text = converter.convert(text)

        # 發票號碼 (2 個大寫字母 + 8 個數字)
        if re.match(r"[A-Z]{2}\d{8}", text):
            extracted_info["TID"] = text

        # 統一編號 (8 碼數字)
        elif "統一編號：" in text or re.match(r"\d{8}", text):
            extracted_info["No"] = re.search(r"\d{8}", text).group()

        # 日期時間格式修正 (修正格式為 YYYY-MM-DD HH:MM:SS)
        elif re.match(r"\d{4}/\d{2}/\d{2}\d{2}:\d{2}:\d{2}", text):
            fixed_date = text[:10].replace("/", "-") + " " + text[10:]
            extracted_info["time"] = fixed_date

        # 總金額
        elif "現金費" in text:
            amount = re.search(r"\d+", text)
            if amount:
                extracted_info["money"] = amount.group()

    return extracted_info