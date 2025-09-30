import io
import os
import requests
import json
import re
import time

import base64
import cv2
import numpy as np
import opencc
import threading
from functools import lru_cache
from core.upload_utils import BASE_DIR, INVOICE_UPLOAD_FOLDER
from keras.models import load_model
from model.parser_model import save_error, save_ocr_result, save_qrcode_result
from paddleocr import PaddleOCR
from PIL import Image
from pyzbar.pyzbar import decode
from qreader import QReader


# === TF GPU 設定 ===
try:
    import tensorflow as tf
    gpus = tf.config.list_physical_devices('GPU')
    for g in gpus:
        tf.config.experimental.set_memory_growth(g, True)
except Exception:
    pass


# 初始化語言轉換器
converter = opencc.OpenCC("s2t")


# 初始化模型
@lru_cache(maxsize=1)
def get_ocr(device: str = "gpu"):
    start = time.time()
    print(f"[OCR] 初始化模型 (device = {device})...", flush=True)

    ocr = PaddleOCR(
        device=device,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        lang="ch",
    )

    elapsed = time.time() - start
    print(f"[OCR] 模型載入完成，用時 {elapsed:.2f} 秒", flush=True)
    return ocr


# 單例模型載入（確保全域只載一次）
_snn_lock = threading.Lock()
_snn_model = None

def get_snn_model():
    global _snn_model
    if _snn_model is None:
        _snn_model = tf.keras.models.load_model("invoice_single_classifier_siamese.keras")
    return _snn_model


# 系統定義的 Type 對應
class_map = {
    0: 3,  # electronic → Type 3
    1: 6,  # receipt → Type 6
    2: 5,  # three_part → Type 5
    3: 2,  # traditional → Type 2
    4: 4   # two_part → Type 4
}


def load_and_preprocess_image(path, img_height=128, img_width=128):
    image = tf.io.read_file(str(path))
    if str(path).lower().endswith(('.jpg', '.jpeg')):
        image = tf.image.decode_jpeg(image, channels=3)
    else:
        image = tf.image.decode_png(image, channels=3)
    image = tf.image.resize(image, [img_height, img_width])
    image = tf.cast(image, tf.float32) / 255.0
    return np.expand_dims(image, axis=0)


def snn_logic(image_path: str, threshold: float = 0.5) -> int:
    try:
        # 載入模型
        model = get_snn_model()

        # 前處理圖片
        img_array = load_and_preprocess_image(image_path)

        # 預測
        with _snn_lock:
            pred = model.predict(img_array, verbose=0)

        predicted_index = int(np.argmax(pred, axis=1)[0])
        confidence = float(np.max(pred))

        # 若信心度太低，視為失敗
        # if confidence < threshold:
        #     return 0

        # 依照系統 class_map 轉換成 Type
        return class_map.get(predicted_index, 0)

    except Exception as e:
        print("推論錯誤:", e)
        return 0


# 呼叫 Ollama 進行結構化
def ai_parse_invoice(ocr_text: str):
    prompt = f"""
    你是一個票據辨識助手。請根據以下 OCR 文字，輸出 JSON 格式。

    輸出 JSON：
    {{
      "invoice_number": "string or null",
      "date": "YYYY-MM-DD or null",
      "total_money": "number or null",
      "items": [
        {{"title": "string", "money": number}}
      ]
    }}

    如果某欄位缺失，請填 null。
    OCR 文字如下：
    {ocr_text}
    """

    # 加逾時與錯誤處理，避免卡住
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "gemma3:4b", "prompt": prompt, "stream": False},
        timeout=30,
    )
    resp.raise_for_status()
    txt = resp.json().get("response", "").strip()

    # 容錯：有時模型會包 code fence
    if txt.startswith("```"):
        txt = txt.strip("`").strip()
        if txt.startswith("json"):
            txt = txt[4:].strip()
    return json.loads(txt or "{}")


# OCR → Ollama 流程
def ocr_ai_logic(image_path, ticket_id, invoice_type):
    try:
        # (1) OCR（單例）
        ocr_model = get_ocr()
        ocr_result = ocr_model.ocr(str(image_path))

        # (2) 整理文字
        text_lines = [converter.convert(item[1][0]).strip() for item in (ocr_result[0] or [])]
        raw_ocr_text = "\n".join([t for t in text_lines if t])

        # (3) 丟到 Ollama
        try:
            structured_data = ai_parse_invoice(raw_ocr_text)
        except Exception as e:
            print(f"[Ollama 解析失敗] ticket_id={ticket_id}：{e}")
            save_error(ticket_id)
            return

        # (4) 存 DB
        ok = save_ocr_result(ticket_id, invoice_type, structured_data or {})
        if not ok:
            print(f"[警告] OCR 結果存檔失敗 ticket_id={ticket_id}")
            save_error(ticket_id)

    except Exception as e:
        print(f"[OCR_AI 錯誤] ticket_id={ticket_id}：{e}")
        save_error(ticket_id)


def invoice_parser(filename: str, ticket_id: int):
    """
    背景任務：票據解析流程
    - filename: 上傳檔案名稱
    - ticket_id: DB 建立的 ticket 主鍵
    """
    try:
        # 圖片路徑
        image_path = BASE_DIR / INVOICE_UPLOAD_FOLDER / filename
        # 1. 用 SNN 判斷類型
        invoice_type = snn_logic(image_path)
        print(invoice_type)

        # 2. 流程分支
        if invoice_type == 0:
            print(f"[辨識失敗] ticket_id={ticket_id} file={filename}")
            save_error(ticket_id)
            return

        if invoice_type == 3:
            # 電子發票 → QRCode 解析
            qrcode_decoder_logic(image_path, ticket_id, invoice_type)
        else:
            # 其他類型 (2,4,5,6) → OCR + Ollama
            ocr_ai_logic(image_path, ticket_id, invoice_type)

    except Exception as e:
        print(f"[invoice_parser 錯誤] ticket_id={ticket_id}, file={filename}: {e}")
        save_error(ticket_id)


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