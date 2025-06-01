import logging
import os

from core.response import make_response
from fastapi import APIRouter, Header, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from views.bot import register_events_logic

from starlette.exceptions import HTTPException

logger = logging.getLogger(__name__)

linebot_router = APIRouter()

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

register_events_logic(handler, line_bot_api)

@linebot_router.post("/callback", summary="LINE Bot Webhook")
async def callback(request: Request, x_line_signature: str = Header(...)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        logger.warning("[LINE BOT] Invalid signature.")
        raise HTTPException(status_code=400, detail="Invalid")

    logger.info("[LINE BOT] Callback received.")
    return make_response("OK")