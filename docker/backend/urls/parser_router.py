import os
from pathlib import Path

from core.response import make_response
from core.upload_utils import upload_image
from fastapi import APIRouter, File, UploadFile
from starlette.exceptions import HTTPException
from views.parser import ocr_logic, qrcode_decoder_logic, snn_logic

parser_router = APIRouter()


@parser_router.post("/parse_invoice", summary="Parse Invoice", description="上傳發票並存入資料庫")
async def parse_invoice(image: UploadFile = File(...)):
    img_bytes = await image.read()
    image_path = Path(os.getenv("INVOICE_UPLOAD_FOLDER")) / Path(upload_image(image, img_bytes, 1))
    print(image_path)
    # 執行 SNN 處理
    invoice_type = await snn_logic(image_path)

    if invoice_type == 0:
        # 執行 QRCode 解析（電子發票）
        message = await qrcode_decoder_logic(image_path, invoice_type)
    else:
        # 執行 OCR 處理
        message = await ocr_logic(img_bytes, invoice_type)

    return make_response(message)
