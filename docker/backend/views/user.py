import os
import random
import string
from starlette.exceptions import HTTPException

from core.upload_utils import is_valid_image
from model.user_model import (create_user, get_user_by_email, get_user_by_uid,
                              get_user_settings, update_password,
                              update_user_img, update_user_info)
from schemas.user import ModifyUserInfo, UserCreate, UserLogin
from views.auth import create_access_token, hash_password, verify_password
from views.email import send_email
from pathlib import Path


def register_logic(user: UserCreate):
    if not get_user_by_email(user.email):
        user.password = hash_password(user.password)
        tracker = create_user(user.username, user.email, user.password)
        if tracker:
            return "創建成功"
        raise HTTPException(status_code=400, detail="創建失敗")
    raise HTTPException(status_code=400, detail="使用者已存在")

def login_logic(payload: UserLogin):
    user = get_user_by_email(payload.email)

    if not user:
        raise HTTPException(status_code=404, detail="查無使用者")

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="帳號或密碼錯誤")

    # 建立 token，sub 為 user_id（與 get_current_user 對應）
    token = create_access_token(user.user_id)

    return "登入成功", {
        "access_token": token
    }

async def forget_password_logic(email: str):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="找不到對應的帳號")

    # 產生任意新密碼
    chars = string.ascii_letters + string.digits
    new_password =  ''.join(random.choices(chars, k=10))
    # 更新資料庫密碼為新密碼
    update_password(email, hash_password(new_password))

    if await send_email(email, new_password):
        return f"已寄送密碼重設連結到 {email}。"
    raise HTTPException(status_code=500, detail="寄送失敗")

def change_user_info_logic(user, payload: ModifyUserInfo):

    if user.email != payload.email and get_user_by_email(payload.email):
        raise HTTPException(status_code=409, detail="此電子郵件已被其他帳戶使用")

    if payload.new_password:
        stored_password = hash_password(payload.new_password)
    else:
        stored_password = user.password

    # 更新 user 資訊
    if update_user_info(user.user_id, payload.username, payload.email, stored_password):
        return "資料更新成功"

async def upload_user_photo_logic(photo, user_id: int):
    content = await photo.read()
    try:
        # 格式檢查
        filename = is_valid_image(photo, content, 0)

        user = get_user_by_uid(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="找不到使用者")

        old_img = user.img
        if not update_user_img(user_id, filename):
            raise HTTPException(status_code=500, detail="圖片更新失敗")

        # 刪除舊照片
        if old_img:
            old_path = Path(os.getenv("USER_IMAGE_UPLOAD_FOLDER")) / old_img
            if old_path.exists():
                old_path.unlink()

        return "大頭貼上傳成功"

    except Exception as e:
        print(f"[ERROR] 上傳大頭貼失敗：{e}")
        raise HTTPException(status_code=500, detail="伺服器錯誤")

def get_current_user_info_logic(user_id: int):
    user = get_user_by_uid(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="找不到使用者")

    user_info = {
        "username": user.username,
        "email": user.email,
        "img": user.img
    }
    return "取得使用者成功", user_info

def get_current_user_settings_logic(user_id: int):
    user = get_user_settings(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="找不到使用者")

    user_info = {
        "priority": user.priority,
        "theme": user.theme
    }
    return "取得使用者成功", user_info