import os
from flask import Blueprint, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from .events import register_events

linebot_bp = Blueprint('linebot', __name__)

# 初始化 LINE Bot
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

register_events(handler, line_bot_api)

@linebot_bp.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")

    if not signature:
        print("❌ 缺少 X-Line-Signature")
        abort(400)

    body = request.get_data(as_text=True)
    print(f"📦 收到LINE Webhook: {body}")

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"❌ Handler error: {e}")
        abort(400)

    return "OK", 200