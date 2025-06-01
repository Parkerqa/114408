from fastapi import UploadFile

import os
import uuid
from pathlib import Path
from starlette.exceptions import HTTPException

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
MAX_FILE_SIZE_MB = 5  # 最大 5MB

BASE_DIR = Path(__file__).resolve().parent.parent  # /app
USER_IMAGE_UPLOAD_FOLDER = Path(os.getenv("USER_IMAGE_UPLOAD_FOLDER"))
INVOICE_UPLOAD_FOLDER = Path(os.getenv("INVOICE_UPLOAD_FOLDER"))

def is_valid_image(photo: UploadFile, content: bytes):
    ext = photo.filename.rsplit(".", 1)[-1].lower()

    # 副檔名限制
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="不支援的檔案格式")

    # MIME 類型限制
    if not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="請上傳圖片格式檔案")

    # 檔案大小限制
    size_mb = len(content) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"圖片大小不可超過 {MAX_FILE_SIZE_MB}MB")

def upload_image(photo: UploadFile, content: bytes, mode: int) -> str:
    is_valid_image(photo, content)

    if mode == 0:
        upload_folder = USER_IMAGE_UPLOAD_FOLDER
    elif mode == 1:
        upload_folder = INVOICE_UPLOAD_FOLDER

    ext = photo.filename.rsplit(".", 1)[-1].lower()
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = upload_folder / new_filename

    # 儲存新照片
    with open(save_path, "wb") as buffer:
        buffer.write(content)
        buffer.flush()
        os.fsync(buffer.fileno())

    return new_filename
