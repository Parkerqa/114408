import os

from fastapi import APIRouter, Header, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from .events import register_events

router = APIRouter(tags=["LINE Bot"])

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

register_events(handler, line_bot_api)

@router.post("/callback", summary="LINE Bot Webhook")
async def callback(request: Request, x_line_signature: str = Header(...)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        print("❌ Signature 驗證失敗")
        return "Invalid Signature", 400

    return "OK"