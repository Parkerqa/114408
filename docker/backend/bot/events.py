from utils.openai import chat_with_gpt
from database.crud import get_ailog
from linebot.models import MessageEvent, TextMessage, TextSendMessage


def register_events(handler, line_bot_api):

    @handler.add(MessageEvent, message=TextMessage)
    def handle_text(event):
        msg = event.message.text.strip()

        if msg == "說話":
            reply_text = get_ailog()
        elif msg == "你好":
            reply_text = "你好，謝謝小籠包"
        elif msg == "(emoji)":
            reply_text = "這是表情貼圖"
        elif msg.startswith("ai:"):
            prompt = msg[3:].strip()
            reply_text = chat_with_gpt(prompt)
        else:
            reply_text = ("盡請期待")

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )