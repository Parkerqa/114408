import requests
import json
import re
import os
import base64
import cv2
import tensorflow as tf
import numpy as np
# import opencc
import threading
from pathlib import Path
from decimal import Decimal
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from core.upload_utils import BASE_DIR, INVOICE_UPLOAD_FOLDER
from model.parser_model import save_error, save_qrcode_result, load_accounting_items
from PIL import Image
from pyzbar.pyzbar import decode
from qreader import QReader
from keras.models import load_model
# from paddleocr import PPStructureV3
# from functools import lru_cache

# 初始化語言轉換器
# converter = opencc.OpenCC("s2t")

# @lru_cache(maxsize=1)
# def get_ocr():
#     return PPStructureV3(
#         lang="chinese_cht",
#         use_doc_orientation_classify=False,
#         use_doc_unwarping=False,
#         use_textline_orientation=False,
#         use_seal_recognition=False,
#         use_formula_recognition=False,
#         use_region_detection=True,
#         enable_mkldnn=False)


# 單例模型載入（確保全域只載一次）
_snn_lock = threading.Lock()
_snn_model = None

def get_snn_model():
    global _snn_model
    if _snn_model is None:
        model_path = BASE_DIR / "invoice_single_classifier_siamese.keras"
        _snn_model = tf.keras.models.load_model(model_path.as_posix())

        dummy = np.zeros((1, 128, 128, 3), dtype=np.float32)
        _snn_model.predict(dummy, verbose=0)

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
    img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"讀取圖片失敗: {path}")
    if img.shape[-1] == 4:
        img = img[:, :, :3]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (img_width, img_height))
    img = np.asarray(img, dtype=np.float32) / 255.0
    return np.expand_dims(img, axis=0)


def snn_logic(image_path: str) -> int:
    try:
        model = get_snn_model()
        img = load_and_preprocess_image(image_path)
        with _snn_lock:
            pred = model.predict(img)
        predicted_index = int(np.argmax(pred[0]))
        return class_map.get(predicted_index, 0)

    except Exception as e:
        print("推論錯誤:", e)
        return 0


# ---- 本地 LLM 解析 ----
def ai_parse_invoice(ocr_html: str) -> Optional[Dict[str, Any]]:
    """
    使用 LLM 解析 OCR 產生的 HTML (包含 p 標籤與 table) 並進行會計科目分類
    """

    # 1. 讀取會計科目清單
    accounting_items = load_accounting_items()

    items_text = "\n".join(
        [f"- ID:{i['id']} | 代碼:{i['code']} | 名稱:{i['name']}"
         for i in accounting_items]
    )

    # 2. 建構 Prompt
    prompt = (
        "你是一個專業的台灣會計憑證識別專家。請閱讀底下的 HTML 原始碼 (包含標題文字與表格)，"
        "提取關鍵資訊並輸出 JSON。\n\n"

        "### 資料來源特性 (重要)\n"
        "1. **文字沾黏處理**：在 `<p>` 標籤中，欄位名稱與數值可能連在一起。例如 '統一編號：國立臺灣師範大學'，"
        "   這代表 '買受人' 是 '國立臺灣師範大學'，而非統編是大學。請依據語意邏輯切分。\n"
        "2. **日期轉換**：將 '中華民國XX年' 轉換為西元年 (民國年+1911)。若日期缺漏 (如 '6月日')，請填 null 或僅輸出 'YYYY-MM'。\n"
        "3. **數值清洗與驗算**：\n"
        "   - 表格內的 '1140-' 應修正為數字 1140。\n"
        "   - 若 '合計金額' (如 '萬宮...') 與 '明細加總' (1140) 不符且差異微小，請優先信任 **明細加總** 的數值。\n"
        "   - '萬宮'、'5拾' 等雜訊請修正為正確數字 (萬壹、50)。\n"
        "4. **賣方資訊**：通常位於表格下方的 rowspan 區塊 (例如 '免用登票享用章... 統一編號...')，請仔細提取。\n\n"

        "### 輸出 JSON 結構要求\n"
        "{\n"
        '  "ticket": {\n'
        '      "invoice_number": string|null, // 若有發票號碼/收據編號請填此。注意：賣方的 "統一編號" (8碼數字) 不是發票號碼，請勿填入此欄。\n'
        '      "date": string|null,           // 格式 YYYY-MM-DD\n'
        '      "total_money": number|null     // 最終金額 (請以明細計算結果為準)\n'
        "  },\n"
        '  "ticket_detail": [\n'
        '      {"title": string, "money": number} // 產品名稱與金額\n'
        "  ],\n"
        '  "classification": {\n'
        '      "accounting_id": number|null,  // 從科目清單選擇 ID\n'
        '      "accounting_name": string|null,\n'
        '      "reason": string|null          // 分類理由\n'
        "  }\n"
        "}\n\n"

        "### 會計科目清單\n"
        f"{items_text}\n\n"

        "### 待處理 HTML 資料\n"
        f"```html\n{ocr_html}\n```"
    )

    # 3. 呼叫 LLM (使用 Ollama)
    try:
        # 根據你的環境設定 Payload
        payload = {
            "model": "gemma3:4b",  # 建議用 llama3, mistral 或 gpt-4o
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.1
            }
        }

        print(f"正在呼叫 LLM 解析收據 (Model: {payload['model']})...")

        # 呼叫 API
        r = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=120
        )
        r.raise_for_status()

        # 解析回傳
        data = r.json()
        response_text = data.get("response", "")

        # 轉換為 Dict
        result = json.loads(response_text)

        return result

    except json.JSONDecodeError:
        print(f"錯誤: LLM 回傳內容無法解析為 JSON。\n原始回傳: {response_text}")
        return None
    except Exception as e:
        print(f"發生錯誤: {e}")
        return None


# ---- OCR主流程 ----
OCR_SERVER_URL = "http://host.docker.internal:8002/ocr_process"
N8N_URL = os.getenv("N8N_WEBHOOK_URL", "http://host.docker.internal:5678/webhook/validate-invoice")


def ocr_ai_logic(image_path: str, ticket_id: int, invoice_type: int):
    """
    修正後的邏輯：
    1. 呼叫本地 OCR Server 獲取文字資料
    2. 準備 Payload (含會計科目)
    3. 發送給 n8n 進行 LLM 處理
    """

    # 變數初始化，避免後續參照錯誤
    ocr_result_data = None

    print(f"=== 開始處理 Ticket ID: {ticket_id} ===", flush=True)

    # ---------------------------------------------------------
    # Step 1: 執行 OCR (呼叫本地 Server)
    # ---------------------------------------------------------
    try:
        if not os.path.exists(image_path):
            print(f"錯誤: 找不到圖片檔案 {image_path}")
            return None

        with open(image_path, 'rb') as f:
            files = {'file': f}
            print(f"正在請求 OCR Server ({OCR_SERVER_URL})...", flush=True)
            response = requests.post(OCR_SERVER_URL, files=files, timeout=300)

        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                ocr_result_data = result.get("data")
                print("OCR 識別成功！\n", f"OCR_Result:{ocr_result_data}")
            else:
                print(f"OCR Server 回報錯誤: {result.get('message')}")
                return None
        else:
            print(f"OCR Server 連線失敗，狀態碼: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"OCR 連線例外錯誤 (請確認本地 Server 是否開啟): {e}")
        return None

    # ---------------------------------------------------------
    # Step 2: 準備資料 (OCR 結果 + 會計科目)
    # ---------------------------------------------------------
    if not ocr_result_data:
        print("錯誤: OCR 處理失敗或無內容，中止後續 n8n 請求")
        return None

    try:
        ocr_html = json.dumps(ocr_result_data, ensure_ascii=False)

        # 讀取會計科目清單
        accounting_items = load_accounting_items()

        payload = {
            "ocr_html": ocr_html,
            "accounting_items": accounting_items,
            "ticket_id": ticket_id,
            "invoice_type": invoice_type,
        }

        # ---------------------------------------------------------
        # Step 3: 發送 POST 請求給 n8n
        # ---------------------------------------------------------
        print(f"正在發送資料給 n8n ({N8N_URL})...", flush=True)

        # timeout 建議設長一點，因為 n8n 後面的 LLM 可能跑很久
        response = requests.post(N8N_URL, json=payload, timeout=120)

        # 檢查 HTTP 狀態碼是否為 200-299
        response.raise_for_status()

        print("n8n 處理完成，已接收回傳資料。")

        return None

    except requests.exceptions.Timeout:
        print("錯誤: n8n 處理逾時 (LLM Timeout)")
        return None
    except requests.exceptions.RequestException as e:
        print(f"錯誤: 無法連線到 n8n Webhook: {e}")
        if e.response is not None:
            print(f"n8n 回應內容: {e.response.text}")
        return None
    except Exception as e:
        print(f"發生未預期錯誤: {e}")
        import traceback
        traceback.print_exc()
        return None


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
    try:
        return int(val, 16)
    except ValueError:
        print(f"[警告] 左碼金額格式無法解析: {val}")
        return 0
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
                    "seller_id": result.get("seller_id"),
                    "buyer_id": result.get("buyer_id"),
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
        print(f"[invoice_parser 錯誤] ticket_id={ticket_id}, file={filename}: {e}", flush=True)
        save_error(ticket_id)