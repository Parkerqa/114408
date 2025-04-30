from dotenv import load_dotenv
from flask import Flask

# 載入環境變數
load_dotenv()

# 初始化 Flask app
app = Flask(__name__)
app.config["TITLE"] = "TicketTransformer"
app.config["DESCRIPTION"] = "整合 LINE Bot 與 OpenAI 的智慧服務"
app.config["VERSION"] = "1.0"

# --- Line Bot ---
from bot.routes import linebot_bp
app.register_blueprint(linebot_bp)

# --- OpenAI ---
from router.openai import openai_bp
app.register_blueprint(openai_bp, url_prefix="/openai")

# --- OCR ---
from router.ocr import ocr_bp
app.register_blueprint(ocr_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=True)