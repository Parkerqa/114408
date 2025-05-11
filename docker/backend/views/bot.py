import logging

from linebot.models import MessageEvent, TextMessage, TextSendMessage

from model.bot_model import get_ticket_by_uid
from views.openai import chat_with_gpt_logic

logger = logging.getLogger(__name__)

# 預設回覆 "收到訊息詞": "回覆訊息詞"
PREDEFINED_RESPONSES = {
    "你好": "你好，謝謝小籠包",
    "(emoji)": "這是表情貼圖",
}

# 訊息回覆
def get_reply_text(msg: str):
    try:
        msg = msg.strip()

        if msg.startswith("查詢:"):
            try:
                uid = int(msg.split(":")[1])
                return get_ticket_by_uid(uid)
            except ValueError:
                return "請提供正確的 uid 數字格式"

        if msg.startswith("ai:"):
            prompt = msg[3:].strip()
            return chat_with_gpt(prompt)

        return PREDEFINED_RESPONSES.get(msg, "盡請期待")

    except Exception as e:
        logger.warning(f"[LINE BOT] 回覆錯誤：{e}")
        return "處理過程中發生錯誤，請稍後再試"

def register_events_logic(handler, line_bot_api):
    @handler.add(MessageEvent, message=TextMessage)
    def handle_text(event):
        msg = event.message.text.strip()
        reply_text = get_reply_text(msg) or "請稍後再試"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )