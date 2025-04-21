from database.crud import post_ticket_detail
from database.db_utils import get_db
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from utils.ocr import extract_invoice_info, run_ocr

router = APIRouter(tags=["PaddleOCR"])

@router.post("/ocr", summary="Service for Paddle OCR", description="上傳發票並存入資料庫")
async def ocr(image: UploadFile =File(...), db: Session = Depends(get_db)):
    content = await image.read()
    # 進行 ocr
    ocr_result = run_ocr(content)

    # 提取發票資訊
    catch_result = extract_invoice_info(ocr_result)

    return post_ticket_detail(db, catch_result)

    # 測試回覆值
    # return catch_result