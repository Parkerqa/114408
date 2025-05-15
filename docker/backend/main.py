import datetime
import logging
import os
import secrets

from core.response import register_exception_handlers
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials

load_dotenv()

logging.basicConfig(filename="docs_access.log", level=logging.INFO)

app = FastAPI(title="TicketTransformer", description="整合 LINE Bot 與 OpenAI 的智慧服務", version="1.0",
              docs_url=None, redoc_url=None, openapi_url=None)

# === CORS setting ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === docs security setting (for dev) ===
def log_docs_access(request: Request, username: str):
    ip = request.client.host
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[DOCS ACCESS] {now} - User: {username} - IP: {ip}")

security = HTTPBasic()
DOCS_USER = os.getenv("DOCS_USER")
DOCS_PASS = os.getenv("DOCS_PASS")

def check_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if not credentials.username or not credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Missing credentials",
            headers={"WWW-Authenticate": "Basic"}
        )
    if not (
        secrets.compare_digest(credentials.username, DOCS_USER) and
        secrets.compare_digest(credentials.password, DOCS_PASS)
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"}
        )
    return True

@app.get("/docs", include_in_schema=False)
async def custom_docs(auth: bool = Depends(check_basic_auth)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Protected Docs")

@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi(auth: bool = Depends(check_basic_auth)):
    return get_openapi(title=app.title, version="1.0.0", routes=app.routes)


# === response ===
from core.response import response_router

app.include_router(response_router)

register_exception_handlers(app)


# === user management ===
from urls.user_router import user_router

app.include_router(user_router, tags=["使用者管理"], prefix="/user")

# === ticket management ===
from urls.ticket_router import ticket_router

app.include_router(ticket_router, tags=["發票管理"], prefix="/ticket")

# === accounting settings ===
from urls.accounting_router import accounting_router

app.include_router(accounting_router, tags=["會計科目管理"], prefix="/accounting")

# === class management ===
from urls.class_router import class_router

app.include_router(class_router, tags=["類別管理"], prefix="/class")

# === settings ===
from urls.setting_router import setting_router

app.include_router(setting_router, tags=["個人化設定"], prefix="/setting")

# === services ===

# linebot
from urls.bot_router import linebot_router

app.include_router(linebot_router, tags=["Line Bot"])

# openai
from urls.openai_router import openai_router

app.include_router(openai_router, tags=["ChatGPT"], prefix="/services")

# ocr
from urls.ocr_router import ocr_router

app.include_router(ocr_router, tags=["Paddle OCR"], prefix="/services")
