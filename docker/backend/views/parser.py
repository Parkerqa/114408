import io
import json
import re

import base64
import cv2
import numpy as np
import opencc
from core.upload_utils import BASE_DIR, INVOICE_UPLOAD_FOLDER
from keras.models import load_model
from model.parser_model import save_error, save_ocr_result, save_qrcode_result
from paddleocr import PaddleOCR
from PIL import Image
from pyzbar.pyzbar import decode
from views.openai import ocr_correction_logic
from qreader import QReader


# 初始化模型
def get_ocr():
    return PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        lang="ch",
    )


# 初始化語言轉換器
converter = opencc.OpenCC("s2t")


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


HEX_CHARS = set("0123456789abcdefABCDEF")

# ---------------- 工具函式 ---------------- #
def decode_item_name(name: str, encoding_flag: str) -> str:
    """中文編碼參數：0=Big5, 1=UTF-8, 2=Base64(UTF-8), 3=UTF-8(境外電商)"""
    try:
        if encoding_flag == "0":
            return name.encode("latin1").decode("big5", errors="ignore")
        elif encoding_flag in ("1", "3"):
            return name
        elif encoding_flag == "2":
            return base64.b64decode(name).decode("utf-8", errors="ignore")
        return name
    except Exception:
        return name


def parse_overseas_amount(val: str) -> float:
    """境外金額(10)：前8碼整數(16進位)+後2碼小數(16進位)"""
    if len(val) != 10 or any(c not in HEX_CHARS for c in val):
        raise ValueError(f"境外金額格式錯誤: {val}")
    integer = int(val[:8], 16)
    decimal = int(val[8:], 16)
    return float(f"{integer}.{decimal:02d}")


def split_ext_fields(left_data: str, right_data: str):
    """切割 77 碼後延伸欄位，以冒號分隔"""
    tail_left = left_data[77:] if len(left_data) > 77 else ""
    tail_right = right_data[2:] if right_data.startswith("**") else right_data
    merged = (tail_left or "") + (tail_right or "")
    fields = merged.split(":") if merged else []
    if fields and fields[0] == "":
        fields = fields[1:]
    return fields


def parse_decimal(s: str):
    """品項數量/單價 → 十進制整數或小數"""
    s = s.strip()
    if not s:
        return 0
    return float(s) if "." in s else int(s)


# ---------------- QRCode 擷取 ---------------- #
def extract_qrcodes(image_path: str, debug: bool = False):
    qreader = QReader()
    img_cv = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    decoded_texts = qreader.detect_and_decode(image=img_cv)

    results = [t for t in decoded_texts if t]

    # fallback: pyzbar
    if len(results) < 2:
        pil_img = Image.open(image_path)
        qrs = decode(pil_img)
        results += [qr.data.decode("utf-8") for qr in qrs]

    # fallback: 左右裁切再用 QReader
    if len(results) < 2:
        h, w = img_cv.shape[:2]
        left_img = img_cv[:, :w // 2]
        right_img = img_cv[:, w // 2:]
        left_data = qreader.detect_and_decode(image=left_img)
        right_data = qreader.detect_and_decode(image=right_img)
        if left_data and isinstance(left_data, list) and left_data[0]:
            results.append(left_data[0])
        if right_data and isinstance(right_data, list) and right_data[0]:
            results.append(right_data[0])

    # 過濾掉太短的雜訊（小於 20 碼）
    results = [r for r in results if len(r) >= 20]

    if debug:
        print("偵測到的 QRCode：")
        for i, qr in enumerate(results):
            print(f"  QR[{i}] 長度={len(qr)}, 開頭={qr[:12]}...")

    if not results:
        raise ValueError("沒有偵測到 QRCode")

    # 確認左右碼角色：左碼必須 >= 77 碼
    if len(results) == 2:
        if len(results[0]) >= 77:
            left_data, right_data = results[0], results[1]
        else:
            left_data, right_data = results[1], results[0]
        return [left_data, right_data]

    return results


# ---------------- 左碼解析 ---------------- #
def parse_amount_8(val: str) -> int | None:
    if val.isdigit():
        return int(val)
    try:
        return int(val, 16)  # fallback：十六進位
    except ValueError:
        print(f"[警告] 左碼金額格式無法解析: {val}")
        return None

def parse_left_qrcode(left_data: str) -> dict:
    if len(left_data) < 77:
        raise ValueError(f"左碼長度不足 77 碼: {left_data}")
    return {
        "invoice_number": left_data[0:10],
        "date": left_data[10:17],
        "random_code": left_data[17:21],
        "sales_amount_8": parse_amount_8(left_data[21:29]),
        "total_amount_8": parse_amount_8(left_data[29:37]),
        "buyer_id": left_data[37:45],
        "seller_id": left_data[45:53],
        "encrypt": left_data[53:77],
    }


# ---------------- 延伸區/右碼解析 ---------------- #
def parse_invoice_ext(left_data: str, right_data: str):
    fields = split_ext_fields(left_data, right_data)
    result = {
        "Details": [],   # 只保留 title 和 money
        "overseas_sales": None,
        "overseas_total": None,
        "encoding": None
    }

    if not fields or len(fields) < 4:
        return result

    overseas = (fields[3] == "3")
    if overseas:
        result["encoding"] = "3"
        if len(fields) > 5:
            try:
                result["overseas_sales"] = parse_overseas_amount(fields[4])
            except Exception as e:
                print("境外銷售額解析錯誤:", e)
            try:
                result["overseas_total"] = parse_overseas_amount(fields[5])
            except Exception as e:
                print("境外總計額解析錯誤:", e)
        start_idx = 6
    else:
        result["encoding"] = fields[3]
        start_idx = 4

    # 品項解析，只保留 title 和 money
    items_raw = fields[start_idx:]
    for i in range(0, len(items_raw), 3):
        if i + 2 >= len(items_raw):
            break
        try:
            title = decode_item_name(items_raw[i], result["encoding"] or "1")
            money = parse_decimal(items_raw[i + 2])
            result["Details"].append({"title": title, "money": money})
        except Exception:
            continue

    return result


# ---------------- 主流程 ---------------- #
def qrcode_decoder_logic(image_path, ticket_id, invoice_type, debug=False):
    try:
        qrcodes = extract_qrcodes(image_path, debug=debug)
        if len(qrcodes) == 2:
            left_data, right_data = qrcodes
        elif len(qrcodes) == 1:
            left_data, right_data = qrcodes[0], ""
        else:
            raise ValueError("無效的 QRCode 數量")

        result = parse_left_qrcode(left_data)
        ext_result = parse_invoice_ext(left_data, right_data)
        result.update(ext_result)

        # 日期轉換 (民國 → 西元)
        raw_date = result.get("date")
        formatted_date = None
        if raw_date and re.match(r"\d{7}", raw_date):
            year = int(raw_date[:3]) + 1911
            month = raw_date[3:5]
            day = raw_date[5:7]
            formatted_date = f"{year}-{month}-{day}"
        result["date"] = formatted_date

        # 總金額決策
        if result.get("overseas_total") is not None:
            total_money = result["overseas_total"]
        elif result.get("items"):
            total_money = sum(item["money"] for item in result["items"])
        elif result.get("total_amount_8") is not None:
            total_money = result["total_amount_8"]
        else:
            total_money = 0

        # 儲存
        if save_qrcode_result(
                ticket_id,
                invoice_type,
                {
                    "invoice_number": result.get("invoice_number"),
                    "date": result.get("date"),
                    "total_money": total_money,
                },
                result.get("Details", []),
        ):
            return
        save_error(ticket_id)

    except Exception as e:
        print("解析錯誤:", e)
        save_error(ticket_id)


def extract_clean_json(content: str) -> str:
    match = re.search(r"\{[\s\S]*?\}", content)
    if match:
        return match.group(0)
    return content


def ocr_logic(image_path, ticket_id, invoice_type):
    try:
        # 步驟 1：執行 OCR，得到原始文字塊
        ocr_model = get_ocr()
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
        image_path = (
            BASE_DIR / INVOICE_UPLOAD_FOLDER / filename
        )  # /app/static/invoice/filename

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
