import logging
import time
import json
import requests
from typing import Optional, Any, Dict, List, Union

from linebot.models import (ImageSendMessage, MessageEvent, TextMessage,
                            TextSendMessage)
from model.bot_model import (get_awaiting_list_by_uid,
                             get_awaiting_ticket_by_uid,
                             get_awaiting_ticket_info_by_uid)
from views.openai import chat_with_gpt_logic

logger = logging.getLogger(__name__)

# 預設回覆 "收到訊息詞": "回覆訊息詞"
PREDEFINED_RESPONSES = {
    "你好": "你好，謝謝小籠包",
    "(emoji)": "這是表情貼圖",
    "待審核的報帳": "awaiting",
    "我想要知道一般報帳走流程的天數大概是多少": "報帳流程所需的天數大概在3–7 天內",
    "我想知道為甚麼這個月的活動費開銷這麼多": "依據圖表來看，您的活動費用有一大部分被使用於臨時團建"
}


# === 環境變數 ===
N8N_RAG_ENDPOINT_RAG = "https://n8n.micky.codes/webhook/rag/chat"

N8N_RAG_ENDPOINT_FINAL = "https://n8n.micky.codes/webhook/ask-final"

BOT_PROXY_KEY = "some-secret"
RAG_WAIT_TTL_SEC = 600


# === 超簡易 in-memory session（可換成 Redis）===
_SESS = {}
def _now(): return int(time.time())
def set_session(uid, data): _SESS[uid] = {**data, "expire_at": _now() + RAG_WAIT_TTL_SEC}
def get_session(uid):
    rec = _SESS.get(uid)
    if not rec or _now() > rec.get("expire_at", 0): _SESS.pop(uid, None); return None
    return rec
def del_session(uid): _SESS.pop(uid, None)

def _coerce_to_text_from_message_field(msg_field):
    """
    將 message 欄位可能的型別統一成文字：
    - str: 直接回傳
    - list[dict]: 嘗試取其中的 {type:'text', text:'...'} 串接
    - list[str]: 串接
    - 其他: 轉成字串
    """
    if isinstance(msg_field, str):
        return msg_field
    if isinstance(msg_field, list):
        texts = []
        for m in msg_field:
            if isinstance(m, dict):
                # LINE 常見 {type:'text', text:'...'}
                if m.get("type") == "text" and isinstance(m.get("text"), str):
                    texts.append(m["text"])
                # 其他鍵值也嘗試抓字串
                elif isinstance(m.get("message"), str):
                    texts.append(m["message"])
            elif isinstance(m, str):
                texts.append(m)
        if texts:
            return "\n".join(texts)
        return str(msg_field)
    return str(msg_field)

def _parse_data_field(data_field):
    """
    嘗試把 data 欄位解析成可讀文字：
    - 若是 JSON 字串/物件：轉成較易讀的字串
    - 若是像 "[object Object]"：直接忽略（回空字串）
    """
    if not data_field:
        return ""
    if isinstance(data_field, (dict, list)):
        try:
            return json.dumps(data_field, ensure_ascii=False, indent=2)
        except Exception:
            return str(data_field)
    if isinstance(data_field, str):
        s = data_field.strip()
        # 避免 "[object Object]" 垃圾字串
        if s.lower().startswith("[object object]"):
            return ""
        # 嘗試 JSON 解析
        if (s.startswith("{") and s.endswith("}")) or (s.startswith("[") and s.endswith("]")):
            try:
                obj = json.loads(s)
                return json.dumps(obj, ensure_ascii=False, indent=2)
            except Exception:
                pass
        return s
    return str(data_field)

def call_n8n_rag(user_id: int, kb: str, question: str, timeout_sec: int = 25) -> str:
    payload = {
        "userId": user_id,
        "mode": "rag",
        "question": question,  # 新工作流使用 question
        "meta": {"kb": kb, "source": "line", "lang": "zh-Hant"}
    }
    headers = {"Content-Type": "application/json"}
    if BOT_PROXY_KEY:
        headers["x-bot-key"] = BOT_PROXY_KEY

    r = requests.post(N8N_RAG_ENDPOINT_RAG, data=json.dumps(payload), headers=headers, timeout=timeout_sec)
    r.raise_for_status()

    # ---- 解析回傳 ----
    text_out = None
    if r.text:
        try:
            data = r.json()
        except ValueError:
            # 非 JSON，直接當純文字
            return r.text.strip()

        # 1) 回傳是 list（你目前的新 n8n 就是這種）
        if isinstance(data, list) and data:
            first = data[0]
            if isinstance(first, dict):
                # 先拿 message
                if "message" in first:
                    text_out = _coerce_to_text_from_message_field(first["message"])
                # 若沒有明確 message，嘗試 text
                if (not text_out or not text_out.strip()) and "text" in first:
                    text_out = str(first["text"])
                # 補充：若 message 很短或空，且 data 有內容就附上（排除 [object Object]）
                data_blob = _parse_data_field(first.get("data"))
                if (not text_out or not text_out.strip()) and data_blob:
                    text_out = data_blob
                elif data_blob and data_blob != "[object Object]":
                    # 視情況把 data 當附註加上
                    text_out = (text_out or "").rstrip() + ("\n\n" if text_out else "") + data_blob

        # 2) 回傳是 dict（相容舊格式）
        elif isinstance(data, dict):
            # 常見舊 RAG：{messages:[...]} 或 {message:[...]} 或 {text:"..."}
            for key in ("messages", "message"):
                if key in data:
                    text_out = _coerce_to_text_from_message_field(data[key])
                    break
            if (not text_out or not text_out.strip()) and "text" in data:
                text_out = str(data["text"])
            if (not text_out or not text_out.strip()) and "data" in data:
                text_out = _parse_data_field(data["data"])

    # fallback
    final_text = (text_out or "（RAG 沒有回傳內容）").strip()
    # 清掉多餘空白/換行
    return final_text if final_text else "（RAG 沒有回傳內容）"


def _pick_text_from_item(item: dict) -> str:
    """
    依優先序取文字：
    1) data（若為可用字串）
    2) message（字串或 LINE 風格的 [{type:'text', text:'...'}]）
    """
    def _clean(s: str) -> str:
        if not isinstance(s, str):
            return ""
        s = s.strip()
        # 忽略無意義的 "[object Object]"
        if s.lower().startswith("[object object]"):
            return ""
        return s

    # 優先用 data
    data_val = item.get("data")
    if isinstance(data_val, str):
        data_txt = _clean(data_val)
        if data_txt:
            return data_txt
    elif isinstance(data_val, (dict, list)):
        try:
            dumped = json.dumps(data_val, ensure_ascii=False)
            if dumped:
                return dumped
        except Exception:
            pass

    # 退回用 message
    msg_val = item.get("message")
    if isinstance(msg_val, str):
        msg_txt = _clean(msg_val)
        if msg_txt:
            return msg_txt
    elif isinstance(msg_val, list):
        texts = []
        for m in msg_val:
            if isinstance(m, dict) and m.get("type") == "text" and isinstance(m.get("text"), str):
                t = _clean(m["text"])
                if t:
                    texts.append(t)
            elif isinstance(m, str):
                t = _clean(m)
                if t:
                    texts.append(t)
        if texts:
            return "\n".join(texts)

    # 最後再試 text 欄
    text_val = item.get("text")
    if isinstance(text_val, str):
        t = _clean(text_val)
        if t:
            return t

    return ""

def call_n8n_final(user_id: int, kb: str, question: str, timeout_sec: int = 25) -> str:
    payload = {
        "question": question,   # 新 workflow 主要吃這個欄位
        "userId": user_id,
        "source": "line",
        "kb": kb,
    }
    headers = {"Content-Type": "application/json"}
    if BOT_PROXY_KEY:
        headers["x-bot-key"] = BOT_PROXY_KEY

    r = requests.post(
        N8N_RAG_ENDPOINT_FINAL,
        data=json.dumps(payload),
        headers=headers,
        timeout=timeout_sec,
    )
    r.raise_for_status()

    if not r.text:
        return "（沒有回傳內容）"

    try:
        data = r.json()
    except ValueError:
        # 非 JSON，直接回純文字
        return r.text.strip() or "（沒有回傳內容）"

    # 回傳可能是 list 或 dict
    if isinstance(data, list):
        texts = []
        for item in data:
            if isinstance(item, dict):
                picked = _pick_text_from_item(item)
                if picked:
                    texts.append(picked)
        if texts:
            return ("\n\n".join(texts)).strip()
        return "（沒有回傳內容）"

    if isinstance(data, dict):
        picked = _pick_text_from_item(data)
        return picked or "（沒有回傳內容）"

    return "（沒有回傳內容）"


# 訊息回覆
def get_reply_text(msg: str, user_id: int = 1):
    try:
        msg = msg.strip()

        if msg.startswith("圖片"):
            try:
                ticket_id = int(msg.replace("圖片", "").strip())
                image_url = get_awaiting_ticket_by_uid(user_id, ticket_id)
                if image_url:
                    return ImageSendMessage(
                        original_content_url=image_url,
                        preview_image_url=image_url
                    )
                else:
                    return TextSendMessage(text="查無對應圖片或尚未上傳")
            except ValueError:
                return TextSendMessage(text="使用者驗證錯誤")

        if msg.startswith("明細"):
            try:
                ticket_id = int(msg.replace("明細", "").strip())
                ticket_info = get_awaiting_ticket_info_by_uid(user_id, ticket_id)
                return TextSendMessage(text=ticket_info)
            except ValueError:
                return TextSendMessage(text="使用者驗證錯誤")

        if msg.startswith("ai:"):
            prompt = msg[3:].strip()
            return TextSendMessage(text=chat_with_gpt_logic(prompt))

        # ---- 進入等待： RAG 問答 ----
        if msg.startswith("RAG 問答"):
            kb = "default"
            if ":" in msg:
                kb = msg.split(":", 1)[1].strip() or "default"
            set_session(user_id, {"mode": "rag_old", "kb": kb, "awaiting": True, "started_at": _now()})
            return TextSendMessage(text=f"已進入「RAG 問答」知識庫：{kb}\n請輸入你的問題（或輸入「取消」離開）")

        # ---- 進入等待：支出佔比分析 ----
        if msg.startswith("支出佔比分析"):
            kb = "default"
            if ":" in msg:
                kb = msg.split(":", 1)[1].strip() or "default"
            set_session(user_id, {"mode": "rag_new", "kb": kb, "awaiting": True, "started_at": _now()})
            return TextSendMessage(text=f"已進入「支出佔比分析」：{kb}\n請輸入你的問題（或輸入「取消」離開）")

        # ---- 取消 ----
        if msg in ("取消", "cancel", "退出"):
            del_session(user_id)
            return TextSendMessage(text="已取消流程。")

        # ---- 等待中的第二步：把本次訊息當問題，依 mode 分流打不同的 n8n ----
        sess = get_session(user_id)
        if sess and sess.get("awaiting") and sess.get("mode") in ("rag_old", "rag_new"):
            question = msg
            kb = sess.get("kb", "default")
            mode = sess.get("mode")
            set_session(user_id, {**sess, "awaiting": False, "last_q": question})
            try:
                if mode == "rag_old":
                    ans = call_n8n_rag(user_id, kb, question, timeout_sec=25)
                else:
                    ans = call_n8n_final(user_id, kb, question, timeout_sec=25)
                set_session(user_id, {**sess, "awaiting": False, "last_q": question, "last_a": ans})
                return TextSendMessage(text=ans)
            except requests.Timeout:
                return TextSendMessage(text="我正在為你檢索資料，稍後把結果傳給你！")
            except Exception as e:
                print("[RAG ERROR]", e)
                return TextSendMessage(text="抱歉，暫時無法取回答案，請稍後再試或重新輸入指令。")

        # ---- 其他預設回覆 ----
        response = PREDEFINED_RESPONSES.get(msg)
        if response == "awaiting":
            try:
                ticket_list = get_awaiting_list_by_uid(user_id)
                return TextSendMessage(text=ticket_list)
            except Exception:
                return TextSendMessage(text="使用者驗證錯誤")
        return TextSendMessage(text=response or "盡請期待")

    except Exception as e:
        logger.warning(f"[LINE BOT] 回覆錯誤：{e}")
        return TextSendMessage(text="處理過程中發生錯誤，請稍後再試")


def register_events_logic(handler, line_bot_api):
    @handler.add(MessageEvent, message=TextMessage)
    def handle_text(event):
        msg = event.message.text.strip()
        reply_message = get_reply_text(msg)

        line_bot_api.reply_message(
            event.reply_token,
            reply_message
        )