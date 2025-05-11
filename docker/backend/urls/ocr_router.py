from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from core.response import make_response
from model.db_utils import get_db
from views.ocr import ocr_logic

ocr_router = APIRouter()

@ocr_router.post("/ocr", summary="Service for Paddle OCR", description="上傳發票並存入資料庫")
async def ocr(image: UploadFile = File(...)):
    try:
        # 執行 OCR 處理
        message, state, status_code = await ocr_logic(image)

        return make_response(message, state, status_code)

    except Exception as e:
        print(f"[ERROR] OCR failed: {e}")
        return make_response("OCR 執行失敗", "error", status_code=500)
