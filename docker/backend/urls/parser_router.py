from core.response import make_response
from fastapi import APIRouter, File, UploadFile
from views.parser import snn_logic, ocr_logic, qrcode_decoder_logic, save_result_logic

parser_router = APIRouter()

@parser_router.post("/parse_invoice", summary="Parse Invoice", description="上傳發票並存入資料庫")
async def parse_invoice(image: UploadFile = File(...)):
    try:
        # 執行 SNN 處理
        snn_message, state, status_code, data = await snn_logic(image)

        if not data:
            return make_response(snn_message, state, status_code)

        if snn_message == 1:
            # 執行 QRCode 解析（電子發票）
            message, state, status_code = qrcode_decoder_logic(data, snn_message)
        else:
            # 執行 OCR 處理
            message, state, status_code = await ocr_logic(data, snn_message)

        return make_response(message, state, status_code)

    except Exception as e:
        print(f"[ERROR] OCR failed: {e}")
        return make_response("發票解析失敗", "error", status_code=500)
