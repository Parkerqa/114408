from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# FastAPI
from api.router import router as api_router
app.include_router(api_router, prefix="/api")

# Linebot
from bot.router import router as linebot_router
app.include_router(linebot_router)