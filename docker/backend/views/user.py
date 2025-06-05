import os
import random
import string
from typing import Optional

from core.upload_utils import BASE_DIR, USER_IMAGE_UPLOAD_FOLDER, upload_image
from fastapi import UploadFile
from model.user_model import (create_user, get_user_by_email, get_user_by_uid,
                              get_user_settings, update_password,
                              update_user_info)
from schemas.user import ModifyUserInfo, UserCreate, UserLogin
from starlette.exceptions import HTTPException
from views.auth import create_access_token, hash_password, verify_password
from views.email import send_email


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
    new_password = ''.join(random.choices(chars, k=10))
    # 更新資料庫密碼為新密碼
    update_password(email, hash_password(new_password))

    if await send_email(email, new_password):
        return f"已寄送密碼重設連結到 {email}。"
    raise HTTPException(status_code=500, detail="寄送失敗")


async def change_user_info_logic(user, payload: ModifyUserInfo, avatar: Optional[UploadFile]):
    if user.email != payload.email and get_user_by_email(payload.email):
        raise HTTPException(status_code=409, detail="此電子郵件已被其他帳戶使用")

    stored_password = hash_password(payload.new_password) if payload.new_password else user.password

    filename = user.img

    old_avatar_path = BASE_DIR / USER_IMAGE_UPLOAD_FOLDER / filename
    if avatar:
        if old_avatar_path.exists() and filename != "user.png":
            try:
                old_avatar_path.unlink()
            except Exception as e:
                print(f"⚠️ 刪除舊頭像失敗：{e}")

        image_bytes = await avatar.read()
        filename = upload_image(avatar, image_bytes, 0)

    # 更新 user 資訊
    if update_user_info(user.user_id, payload.username, payload.email, stored_password, filename):
        return "資料更新成功"


def get_current_user_info_logic(user_id: int):
    user = get_user_by_uid(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="找不到使用者")

    img_url = f'{os.getenv("BASE_USER_IMAGE_URL")}{user.img}' if user.img else None

    user_info = {
        "username": user.username,
        "email": user.email,
        "img": img_url
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
