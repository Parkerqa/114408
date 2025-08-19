from typing import Any, Optional

from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import (HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED,
                              HTTP_422_UNPROCESSABLE_ENTITY,
                              HTTP_500_INTERNAL_SERVER_ERROR)

response_router = APIRouter()


# 統一回傳格式函數
def make_response(message: str = "OK", state: str = "success", status_code: int = 200,
                  data: Optional[Any] = None) -> JSONResponse:
    response = {
        "message": message,
        "state": state,
        "statusCode": status_code,
    }
    if data is not None:
        response["data"] = data
    return JSONResponse(content=response, status_code=status_code)


# 全域錯誤處理註冊函數

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        headers = getattr(exc, "headers", {}) or {}
        # Basic Auth 需要保留 WWW-Authenticate header
        if headers.get("WWW-Authenticate") == "Basic":
            return JSONResponse(
                content={"detail": exc.detail},
                status_code=exc.status_code,
                headers=headers
            )
        # JWT 驗證失敗
        if exc.status_code == 401 and "token" in str(exc.detail).lower():
            return make_response(str(exc.detail), "error", 401)
        if exc.status_code == 401 and "authenticated" in str(exc.detail).lower():
            return make_response("無配置認證", "error", 401)
        # 其餘 HTTP 錯誤
        return make_response(str(exc.detail), "error", exc.status_code)

    @app.exception_handler(HTTP_405_METHOD_NOT_ALLOWED)
    async def method_not_allowed_handler(request: Request, exc):
        return make_response("不允許的請求方法", "error", HTTP_405_METHOD_NOT_ALLOWED)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return make_response("請求參數驗證失敗", "error", HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return make_response("伺服器內部錯誤", "error", HTTP_500_INTERNAL_SERVER_ERROR)
