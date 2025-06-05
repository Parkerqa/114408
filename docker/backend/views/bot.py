import logging

from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from model.bot_model import get_awaiting_ticket_by_uid, get_awaiting_list_by_uid, get_awaiting_ticket_info_by_uid
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

# 訊息回覆
def get_reply_text(msg: str):
    try:
        msg = msg.strip()

        if msg.startswith("圖片"):
            try:
                ticket_id = int(msg.replace("圖片", "").strip())
                image_url = get_awaiting_ticket_by_uid(1, ticket_id)
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
                ticket_info = get_awaiting_ticket_info_by_uid(1, ticket_id)
                return TextSendMessage(text=ticket_info)
            except ValueError:
                return TextSendMessage(text="使用者驗證錯誤")

        if msg.startswith("ai:"):
            prompt = msg[3:].strip()
            return TextSendMessage(text=chat_with_gpt_logic(prompt))


        response = PREDEFINED_RESPONSES.get(msg)

        if response == "awaiting":
            try:
                ticket_list = get_awaiting_list_by_uid(1)
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