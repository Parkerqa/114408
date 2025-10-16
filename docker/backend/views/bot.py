import logging
import time
import json
import requests
from typing import Optional

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


# === 你自己的環境變數/常數 ===
N8N_RAG_ENDPOINT = "https://n8n.micky.codes/webhook-test/rag/chat"
BOT_PROXY_KEY = "some-secret"  # 對 n8n 的簡單驗證(選用)
RAG_WAIT_TTL_SEC = 600         # 等待下一則問題的有效時間(秒)

# === 超簡易 in-memory session（可換成 Redis）===
_SESS = {}  # key: user_id, val: dict
def _now() -> int:
    return int(time.time())

def set_session(user_id: int, data: dict):
    _SESS[user_id] = {**data, "expire_at": _now() + RAG_WAIT_TTL_SEC}

def get_session(user_id: int) -> Optional[dict]:
    rec = _SESS.get(user_id)
    if not rec:
        return None
    if _now() > rec.get("expire_at", 0):
        _SESS.pop(user_id, None)
        return None
    return rec

def del_session(user_id: int):
    _SESS.pop(user_id, None)

def call_n8n_rag(user_id: int, kb: str, question: str, timeout_sec: int = 25) -> str:
    """呼叫 n8n RAG workflow，回傳文字（你也可以改成回傳陣列以支援多訊息）"""
    payload = {
        "userId": user_id,
        "mode": "rag",
        "text": question,
        "meta": {
            "kb": kb,
            "source": "line",
            "lang": "zh-Hant"
        }
    }
    headers = {"Content-Type": "application/json"}
    if BOT_PROXY_KEY:
        headers["x-bot-key"] = BOT_PROXY_KEY

    r = requests.post(N8N_RAG_ENDPOINT, data=json.dumps(payload), headers=headers, timeout=timeout_sec)
    r.raise_for_status()
    data = r.json() if r.text else {}

    # 兼容兩種回傳：{text: "..."} 或 {messages: [{type:'text', text:'...'}, ...]}
    if isinstance(data, dict):
        if "messages" in data and isinstance(data["messages"], list) and data["messages"]:
            # 合併成單段文字；你也可改成回傳多段 LINE 訊息
            texts = []
            for m in data["messages"]:
                if isinstance(m, dict) and m.get("type") == "text" and m.get("text"):
                    texts.append(str(m["text"]))
            if texts:
                return "\n".join(texts)
        if "text" in data and isinstance(data["text"], str):
            return data["text"]

    return "（RAG 沒有回傳內容）"


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

        # === RAG 問答：第一階段（進入等待） ===
        if msg.startswith("RAG 問答"):
            # 支援 "RAG 問答" 或 "RAG 問答:invoice"
            kb = "default"
            seg = msg.split(":", 1)
            if len(seg) == 2 and seg[1].strip():
                kb = seg[1].strip()

            set_session(user_id, {
                "mode": "rag",
                "kb": kb,
                "awaiting_question": True,
                "started_at": _now(),
            })

            hint = f"已進入「RAG 問答」模式（知識庫：{kb}）。\n請直接輸入你的問題。輸入「取消」可離開。"
            return TextSendMessage(text=hint)

        # === RAG 問答：取消 ===
        if msg in ("取消", "cancel", "退出"):
            del_session(user_id)
            return TextSendMessage(text="已取消「RAG 問答」流程。")

        # === RAG 問答：第二階段（等待中 → 當前訊息就是問題，呼叫 n8n） ===
        sess = get_session(user_id)
        if sess and sess.get("mode") == "rag" and sess.get("awaiting_question"):
            question = msg  # 這則當成真正的問題
            kb = sess.get("kb", "default")
            # 先關閉等待（避免重入）
            set_session(user_id, {**sess, "awaiting_question": False, "last_question": question})

            try:
                answer_text = call_n8n_rag(user_id=user_id, kb=kb, question=question, timeout_sec=25)
                # 你可視需要保留最後答案在 session
                set_session(user_id, {**sess, "awaiting_question": False, "last_question": question, "last_answer": answer_text})
                return TextSendMessage(text=answer_text)
            except requests.Timeout:
                # 時間較長時，LINE Reply API 容易逾時；這裡先回覆占位（若你有 Push 通道可再補送正式答案）
                return TextSendMessage(text="我正在為你檢索資料，稍後把結果傳給你！")
            except Exception as e:
                # 任何錯誤都不要讓流程卡死
                print("[RAG ERROR]", e)
                return TextSendMessage(text="抱歉，暫時無法取回答案，請稍後再試或重新輸入「RAG 問答」。")

        # === 其他預設回覆 ===
        response = PREDEFINED_RESPONSES.get(msg)

        if response == "awaiting":
            try:
                ticket_list = get_awaiting_list_by_uid(user_id)
                return TextSendMessage(text=ticket_list)
            except Exception as e:
                print(e)
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