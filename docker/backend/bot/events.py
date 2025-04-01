from linebot.models import MessageEvent, TextMessage, TextSendMessage
from database.crud import get_ailog

def register_events(handler, line_bot_api):

    @handler.add(MessageEvent, message=TextMessage)
    def handle_text(event):
        msg = event.message.text.strip()

        if msg == "說話":
            reply_text = get_ailog()
        elif msg == "你好":
            reply_text = "你好，謝謝小籠包"
        else:
            reply_text = "不支援"
            # try:
            #     response = openai.ChatCompletion.create(
            #         model="gpt-3.5-turbo",  # 或 gpt-4
            #         messages=[
            #             {"role": "system", "content": "你是一個親切的LINE聊天助手，以下對話請用繁體中文回答問題"},
            #             {"role": "user", "content": user_msg}
            #         ]
            #     )
            #     reply_text = response['choices'][0]['message']['content'].strip()
            # except Exception as e:
            #     reply_text = f"GPT 回應失敗：{str(e)}"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )