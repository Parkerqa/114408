import requests
import json
import re
import os
import time

import base64
import cv2
import tensorflow as tf
import numpy as np
import opencc
import threading
from pathlib import Path
from decimal import Decimal
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from functools import lru_cache
from core.upload_utils import BASE_DIR, INVOICE_UPLOAD_FOLDER
from keras.models import load_model
from model.parser_model import save_error, save_ocr_result, save_qrcode_result
from paddleocr import PaddleOCR
from PIL import Image
from pyzbar.pyzbar import decode
from qreader import QReader

# 初始化語言轉換器
# converter = opencc.OpenCC("s2t")
#
# @lru_cache(maxsize=1)
# def get_ocr():
#     return PaddleOCR(
#         device="cpu",
#         use_doc_orientation_classify=False,
#         use_doc_unwarping=False,
#         use_textline_orientation=False
#     )


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


def snn_logic(image_path: str, threshold: float = 0.5) -> int:
    try:
        model = get_snn_model()
        img_array = load_and_preprocess_image(image_path)
        with _snn_lock:
            pred = model.predict(img_array, verbose=0)
        predicted_index = int(np.argmax(pred[0]))
        return class_map.get(predicted_index, 0)

    except Exception as e:
        print("推論錯誤:", e)
        return 0


# ========== HTTP 工具（重試/退避） ==========
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", "120"))

def post_with_retry(url: str, retries: int = 3, backoff: float = 1.7, **kwargs) -> requests.Response:
    last_err = None
    for i in range(retries):
        try:
            r = requests.post(url, timeout=HTTP_TIMEOUT, **kwargs)
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException as e:
            last_err = e
            if i == retries - 1:
                break
            time.sleep(backoff ** i)
    raise last_err


def get_with_retry(url: str, retries: int = 2, backoff: float = 1.7, **kwargs) -> requests.Response:
    last_err = None
    for i in range(retries):
        try:
            r = requests.get(url, timeout=HTTP_TIMEOUT, **kwargs)
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException as e:
            last_err = e
            if i == retries - 1:
                break
            time.sleep(backoff ** i)
    raise last_err


# OCR → Ollama 流程
# === 1) Ollama 連線設定：用環境變數可解決 container DNS 問題 ===
# ========== 連線設定 ==========
# 建議用環境變數覆蓋（以下為預設）
OLLAMA_URL = "http://localhost:11434"
# 你目前寫的是 trycloudflare 臨時網址；建議改成 Named Tunnel 固定域名
CLOUDFLARE_OCR_URL = "https://exploration-parliament-letter-modified.trycloudflare.com/ocr"

# ===================== ① n8n 參數（放在檔案前面區塊） =====================
N8N_VALIDATE_TEST_URL = "https://n8n.micky.codes/webhook-test/validate-invoice"

# 明細策略：你說「只應該一個 title」→ 開 True
SINGLE_DETAIL_MODE = True

# 金額合理上下限（依場景調整）
MIN_MONEY = 1
MAX_MONEY = 2_000_000  # 單項/總金額上限（同時也拿來擋 DB out-of-range）

# ------- 規則常數 -------
TOTAL_KEYWORDS = ["總計", "合計", "應付", "金額", "總額", "現金", "實收"]
META_KEYWORDS  = ["發票", "票", "機", "車", "電話", "統一編號", "統編", "編號", "號碼", "發車", "交易序號", "序號"]
ADDR_TOKENS    = ["路", "街", "巷", "弄", "段", "樓", "號", "里", "鄉", "鎮", "市", "區", "屯", "坪"]
NOISE_TOKENS   = ["Tx", "TX", "率用", "折扣", "折讓", "稅", "稅別", "稅率", "合稅", "未稅"]
ID_PATTERNS = [
    r"\d{2,4}[-–]\d{3,4}[-–]\d{3,4}",  # 電話 02-2582-3333
    r"[A-Z]{2}\d{8}",                  # 統一發票號
    r"[A-Z0-9]{5,8}",                  # 車牌/代碼（寬鬆）
    r"\d{10,}",                        # 10 碼以上長數字
]


def _call_save_ocr_result(ticket_id: int, invoice_type: int, parsed: dict) -> bool:
    try:
        return save_ocr_result(ticket_id, invoice_type, parsed)  # noqa: F821
    except NameError:
        print("[提示] save_ocr_result 尚未匯入，請在專案中導入。")
        return False


def _call_save_error(ticket_id: int):
    try:
        save_error(ticket_id)  # noqa: F821
    except NameError:
        print(f"[提示] save_error 尚未匯入，ticket_id={ticket_id}。")


# ---- 公用小工具 ----
def _norm_date_candidate(s: str) -> Optional[str]:
    s = s.strip()
    m_dt = re.search(r"(\d{4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})[\sT]*(\d{1,2}):(\d{2})(?::(\d{2}))?", s)
    if m_dt:
        y, mo, d, hh, mm, ss = m_dt.groups()
        try:
            dt = datetime(int(y), max(1, min(12, int(mo))), max(1, min(31, int(d))),
                          max(0, min(23, int(hh))), max(0, min(59, int(mm))), int(ss or 0))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
    m_d = re.search(r"(\d{4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})", s)
    if m_d:
        y, mo, d = m_d.groups()
        try:
            dt = datetime(int(y), max(1, min(12, int(mo))), max(1, min(31, int(d))))
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass
    m_tw = re.search(r"(\d{2,3})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})", s)
    if m_tw:
        y, mo, d = m_tw.groups()
        y_adj = int(y) + 1911 if int(y) < 1911 else int(y)
        try:
            dt = datetime(y_adj, max(1, min(12, int(mo))), max(1, min(31, int(d))))
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None


def _is_total_line(t: str) -> bool:
    return any(k in t for k in TOTAL_KEYWORDS)


def _is_meta_like(t: str) -> bool:
    if any(kw in t for kw in META_KEYWORDS):  return True
    if any(tok in t for tok in ADDR_TOKENS):  return True
    if any(tok in t for tok in NOISE_TOKENS): return True
    for pat in ID_PATTERNS:
        if re.search(pat, t): return True
    return False


def _extract_money_robust(t: str, total_money: Optional[int] = None, forbid_equal_total: bool = True) -> Optional[int]:
    """抽最後一個金額；排除地址/票號/電話/稅；避免把總額行當明細。"""
    if _is_meta_like(t):
        return None
    nums = re.findall(r"\d[\d,]*(?:\.\d{1,2})?", t)
    if not nums:
        return None
    val = nums[-1].replace(",", "")
    try:
        money = int(float(val))
    except ValueError:
        return None
    if money < MIN_MONEY or money > MAX_MONEY:
        return None
    if forbid_equal_total and total_money is not None and money == total_money:
        return None
    return money


def _looks_like_invoice_no(s: str) -> bool:
    return bool(re.fullmatch(r"[A-Z]{2}\d{8}", s.strip()))


def make_jsonable(x):
    """把 Path / datetime / Decimal / numpy / bytes 等轉成可 JSON 序列化型別。"""
    # 標量
    if x is None or isinstance(x, (str, int, float, bool)):
        return x
    # Path -> string
    if isinstance(x, Path):
        return str(x)
    # datetime/date -> ISO
    if isinstance(x, (datetime, date)):
        return x.isoformat()
    # Decimal -> float（或改成 str 視需求）
    if isinstance(x, Decimal):
        return float(x)
    # bytes -> base64（或改成 bytes.hex()）
    if isinstance(x, (bytes, bytearray)):
        return base64.b64encode(x).decode("utf-8")
    # numpy 標量/陣列
    if isinstance(x, (np.generic,)):
        return x.item()
    if isinstance(x, (np.ndarray,)):
        return x.tolist()
    # dict / list / tuple / set 遞迴處理
    if isinstance(x, dict):
        return {str(k): make_jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple, set)):
        return [make_jsonable(v) for v in x]
    # 最後退路：字串化
    return str(x)

def safe_json_dumps(obj, **kwargs):
    return json.dumps(make_jsonable(obj), **kwargs)


# ---- 3) LLM 解析（可選）----
def ai_parse_invoice(rec_texts: List[str]) -> Optional[Dict[str, Any]]:
    # 健康檢查略…
    prompt = (
        "你是資料抽取器。請只輸出 JSON（不要任何多餘文字/註解/程式碼圍欄）。\n"
        "結構：{\n"
        '  "ticket": {"invoice_number": string|null, "date": string|null, "total_money": number|null},\n'
        '  "ticket_detail": [{"title": string, "money": number}] \n'
        "}\n"
        "- invoice_number：兩英+八數，如 AB12345678；找不到給 null\n"
        "- date：YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS；找不到給 null\n"
        "- total_money：整數；找不到給 null\n"
        "- ticket_detail：若不確定就給空陣列 []\n"
        "只輸出上述 JSON，不能有其他文字。\n\n"
        f"{json.dumps(rec_texts, ensure_ascii=False)}"
    )

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": os.getenv("OLLAMA_MODEL", "gemma:4b"),
                "prompt": prompt,
                "stream": False,
                "format": "json"  # ←← 重點：強制 JSON
            },
            timeout=60
        )
        r.raise_for_status()
        # 使用 Ollama 的 JSON 格式輸出：r.json() 仍是 {response: "<json-string>"}
        data = r.json()
        text = data.get("response", "")
        return json.loads(text)  # 直接 parse
    except Exception:
        return None


# ---- 4) 本地規則解析（強韌、一定有產出）----
def parse_invoice_locally(rec_texts: List[str]) -> Dict[str, Any]:
    """不把總金額行/地址/票號/電話當明細；明細合計偏離總金額就清空；支援只留一筆。"""
    invoice_number = None
    date_iso = None
    total_money = None
    details: List[Dict[str, Any]] = []

    # A) 先抓發票號、日期、總金額
    for raw in rec_texts:
        t = str(raw).strip()
        if not invoice_number and _looks_like_invoice_no(t):
            invoice_number = t
        if not date_iso:
            d = _norm_date_candidate(t)
            if d: date_iso = d
        if total_money is None and _is_total_line(t):
            m = _extract_money_robust(t, total_money=None, forbid_equal_total=False)
            if m is not None: total_money = m

    # B) 明細（過濾地址/票號/電話/稅/折扣/總額行）
    for raw in rec_texts:
        t = str(raw).strip()
        if _is_total_line(t) or _is_meta_like(t):
            continue
        # 必須同時有中文字與數字
        if not (re.search(r"[一-龥]", t) and re.search(r"\d", t)):
            continue
        money = _extract_money_robust(t, total_money=total_money, forbid_equal_total=True)
        if money is None:
            continue
        title = re.sub(r"[\d,\.]+", "", t)
        title = re.sub(r"[：:，,。．.／/－\-—\s]+$", "", title).strip()
        if len(title) < 2 or _is_meta_like(title):
            continue
        if total_money is not None and money > total_money:
            continue
        details.append({"title": title, "money": money})

    # C) 合理性檢查
    if details and total_money is not None:
        s = sum(d["money"] for d in details)
        if s > total_money or s < int(total_money * 0.6):
            details = []

    # D) 只留一筆（若開啟）
    if SINGLE_DETAIL_MODE:
        if total_money is not None:
            eq = [d for d in details if d["money"] == total_money]
            details = eq[:1] if eq else []
        else:
            details = details[:1] if details else []

    return {
        "ticket": {
            "invoice_number": invoice_number,
            "date": date_iso,
            "total_money": total_money
        },
        "ticket_detail": details
    }


# ---- 5) 取得 OCR（加上逾時 & 錯誤處理）----
def _normalize_ocr_url(url: str) -> str:
    # 支援傳入 base 或已含 /ocr 的完整路徑
    u = url.rstrip("/")
    return u if u.endswith("/ocr") else (u + "/ocr")

def fetch_rec_texts_from_cloud(image_path: str) -> List[str]:
    ocr_url = _normalize_ocr_url(CLOUDFLARE_OCR_URL)
    with open(image_path, "rb") as f:
        files = {"file": (os.path.basename(image_path), f, "application/octet-stream")}
        res = post_with_retry(ocr_url, files=files)
    try:
        data = res.json()
    except ValueError as e:
        raise ValueError(f"OCR 回傳非 JSON：{e}; text={res.text[:200]}")

    # 你的雲端 API 最後是「只回傳純陣列」或包 {"rec_texts": [...]} 兩種都支援
    if isinstance(data, list):
        return [str(x) for x in data]
    if isinstance(data, dict) and "rec_texts" in data:
        return [str(x) for x in data["rec_texts"]]
    raise ValueError(f"無法識別 OCR API 回傳格式：{type(data)} keys={list(data) if isinstance(data, dict) else ''}")


def _build_doc_for_n8n(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """
    將本地解析的巢狀結構，整理成 n8n workflow 期待的 doc 物件。
    你的 workflow 會把 doc stringify 後交給後續節點。
    """
    ticket = parsed.get("ticket") or {}
    details = parsed.get("ticket_detail") or []

    # 確保型別正確（total_money 整數；money 整數）
    def _to_int_safe(x):
        try:
            if x is None: return None
            return int(float(str(x).replace(",", "")))
        except Exception:
            return None

    total_money = _to_int_safe(ticket.get("total_money"))
    sane_details = []
    for d in details:
        if not isinstance(d, dict):
            continue
        title = str(d.get("title") or "").strip()
        money = _to_int_safe(d.get("money"))
        if title and money is not None:
            sane_details.append({"title": title, "money": money})

    return {
        "ticket": {
            "invoice_number": (ticket.get("invoice_number") or "") or None,
            "date": ticket.get("date") or None,
            "total_money": total_money
        },
        "ticket_detail": sane_details
    }


def post_to_n8n(parsed: Dict[str, Any],
                raw_url: str = "",
                preprocessed_url: str = "",
                raw_b64: str = "",
                preprocessed_b64: str = "",
                prompt_overrides: str = "") -> Optional[Dict[str, Any]]:
    url = N8N_VALIDATE_TEST_URL
    if not url:
        print("[n8n] 未設定 N8N_VALIDATE_URL / N8N_VALIDATE_TEST_URL，略過上送。")
        return None

    doc_obj = _build_doc_for_n8n(parsed)
    doc_json_str = safe_json_dumps(doc_obj, ensure_ascii=False)

    payload = {
        "doc": doc_obj,
        "doc_json_str": doc_json_str,
        "images": {
            # 這些如果你傳的是 Path，就會被 make_jsonable 轉成字串
            "raw_url": raw_url or "",
            "preprocessed_url": preprocessed_url or "",
            "raw_b64": raw_b64 or "",
            "preprocessed_b64": preprocessed_b64 or ""
        },
        "gemm3": {"prompt_overrides": prompt_overrides or ""}
    }

    # 重要：payload 先淨化
    payload = make_jsonable(payload)

    r = post_with_retry(url, json=payload, retries=3, backoff=1.7)
    try:
        return r.json()
    except Exception:
        return {"status_code": r.status_code, "text": r.text}


# ---- 6) 主流程（你現有函式替換成這個）----
def ocr_ai_logic(image_path: str, ticket_id: int, invoice_type: int):
    try:
        # (A) 取 OCR 結果（rec_texts）
        rec_texts = fetch_rec_texts_from_cloud(image_path)

        # (B) 保留原始 OCR log（方便除錯）
        try:
            with open("ocr_result.json", "w", encoding="utf-8") as f:
                f.write(safe_json_dumps(rec_texts, ensure_ascii=False, indent=2))
        except Exception:
            pass
        print(json.dumps({"rec_texts": rec_texts}, ensure_ascii=False, indent=2))

        # (C) 嘗試 LLM 解析（可用才用）
        parsed = ai_parse_invoice(rec_texts)

        # (D) LLM 失敗或不可用 → 本地規則解析
        if not parsed:
            parsed = parse_invoice_locally(rec_texts)

        # (E) 寫 DB（若你的專案未匯入 save_ocr_result，會提示）
        ok = _call_save_ocr_result(ticket_id, invoice_type, parsed or {})
        if not ok:
            print(f"[警告] OCR 結果存檔失敗 ticket_id={ticket_id}")
            _call_save_error(ticket_id)

        # === 新增：丟到 n8n（不影響 DB 成功與否；失敗只記 log） ===
        n8n_resp = post_to_n8n(parsed, raw_url=image_path)
        if n8n_resp is not None:
            print("[n8n] 回應：", json.dumps(n8n_resp, ensure_ascii=False, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"[OCR_AI 錯誤] ticket_id={ticket_id}：OCR 連線/逾時失敗 - {e}")
        _call_save_error(ticket_id)
    except Exception as e:
        print(f"[OCR_AI 錯誤] ticket_id={ticket_id}：{e}")
        _call_save_error(ticket_id)


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