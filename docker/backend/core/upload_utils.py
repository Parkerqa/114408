from typing import Tuple

from fastapi import UploadFile

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
MAX_FILE_SIZE_MB = 5  # 最大 5MB

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_image(photo: UploadFile, content: bytes) -> Tuple[bool, str]:
    ext = photo.filename.rsplit(".", 1)[-1].lower()

    # 副檔名限制
    if ext not in ALLOWED_EXTENSIONS:
        return False, "不支援的檔案格式"

    # MIME 類型限制
    if not photo.content_type.startswith("image/"):
        return False, "請上傳圖片格式檔案"

    # 檔案大小限制
    size_mb = len(content) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"圖片大小不可超過 {MAX_FILE_SIZE_MB}MB"

    return True, "OK"