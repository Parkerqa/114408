from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(title="TicketTransformer", description="整合 LINE Bot 與 OpenAI 的智慧服務", version="1.0")

# linebot
from bot.routes import router as linebot_router

app.include_router(linebot_router)

# openai
from router.openai import router as openai_router

app.include_router(openai_router, prefix="/openai")

# ocr
from router.ocr import router as ocrrouter

app.include_router(ocrrouter)