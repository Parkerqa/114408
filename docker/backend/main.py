import datetime
import logging
import os
import secrets
from pathlib import Path

from core.response import register_exception_handlers
from core.upload_utils import INVOICE_UPLOAD_FOLDER, USER_IMAGE_UPLOAD_FOLDER
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles

load_dotenv()

logging.basicConfig(filename="docs_access.log", level=logging.INFO)

app = FastAPI(title="TicketTransformer", description="整合 LINE Bot 與 OpenAI 的智慧服務", version="1.0",
              docs_url=None, redoc_url=None, openapi_url=None)

# === 掛載靜態資源 ===
app.mount("/static", StaticFiles(directory="static"), name="static")


# === 自動重建資料夾的中介層 ===
@app.middleware("http")
async def ensure_static_dirs(request: Request, call_next):
    for folder in [Path("static"), USER_IMAGE_UPLOAD_FOLDER, INVOICE_UPLOAD_FOLDER]:
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
    return await call_next(request)


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
from urls.classinfo_router import classinfo_router

app.include_router(classinfo_router, tags=["類別管理"], prefix="/class")

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

# Parse Invoice
# from urls.parser_router import parser_router
#
# app.include_router(parser_router, tags=["Parse Invoice"], prefix="/services")
