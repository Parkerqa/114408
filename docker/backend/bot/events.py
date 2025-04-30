from router.openai import chat_with_gpt
from database.crud import get_ailog
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 預設回覆 "收到訊息詞": "回覆訊息詞"
PREDEFINED_RESPONSES = {
    "你好": "你好，謝謝小籠包",
    "(emoji)": "這是表情貼圖",
}

# 訊息回覆
def get_reply_text(msg: str) -> str:
    try:
        if msg == "說話":
            return get_ailog()
        elif msg.startswith("ai:"):
            prompt = msg[3:].strip()
            return chat_with_gpt(prompt)
        return PREDEFINED_RESPONSES.get(msg, "盡請期待")
    except Exception as e:
        print(f"[ERROR] Message handling failed: {e}")
        return "處理過程中發生錯誤，請稍後再試"

def register_events(handler, line_bot_api):
    @handler.add(MessageEvent, message=TextMessage)
    def handle_text(event):
        try:
            msg = event.message.text.strip()
            reply_text = get_reply_text(msg)

            print(f"[LineBot] Received: {msg}")
            print(f"[LineBot] Replying: {reply_text}")

            if not reply_text:
                reply_text = "抱歉，我沒聽懂你的意思。"

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
        except Exception as e:
            print(f"[ERROR] LineBot event handling failed: {str(e)}")