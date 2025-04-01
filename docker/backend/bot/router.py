from fastapi import APIRouter, Request, Header
from linebot.exceptions import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
import os
from .events import register_events

router = APIRouter()

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

register_events(handler, line_bot_api)

@router.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(...)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        print("❌ Signature 驗證失敗")
        return "Invalid Signature", 400

    return "OK"