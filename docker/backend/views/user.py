import random
import shutil
import string
import uuid
from pathlib import Path

from core.upload_utils import is_valid_image
from model.user_model import (create_user, get_user_by_email, get_user_by_uid,
                              update_password, update_user_img,
                              update_user_info)
from schemas.user import (ModifyUserInfo, PasswordChange, PasswordForget,
                          UserCreate, UserLogin)
from views.auth import create_access_token, hash_password, verify_password
from views.email import send_email


def register_logic(user: UserCreate):
    if not get_user_by_email(user.email):
        user.password = hash_password(user.password)
        tracker = create_user(user.username, user.email, user.password)
        if tracker:
            return "創建成功", "success", 200
        return "創建失敗", "error", 500
    return "使用者已存在", "error", 400

def login_logic(payload: UserLogin):
    user = get_user_by_email(payload.email)

    if not user:
        return "查無使用者", "error", 404, None

    if not verify_password(payload.password, user.password):
        return "帳號或密碼錯誤", "error", 401, None

    # 建立 token，sub 為 uid（與 get_current_user 對應）
    token = create_access_token(user.uid)

    return "登入成功", "success", 200, {
        "access_token": token
    }

def change_password_logic(user_info, payload: PasswordChange):
    if not verify_password(payload.old_password, user_info.password):
        return "舊密碼錯誤", "error", 401
    email = user_info.email
    if update_password(email, hash_password(payload.new_password)):
        return "密碼已更新成功", "success", 200
    return "更新資料庫失敗", "error", 500

async def forget_password_logic(email: str):
    user = get_user_by_email(email)
    if not user:
        return "找不到對應的帳號", "error", 404

    # 產生任意新密碼
    chars = string.ascii_letters + string.digits
    new_password =  ''.join(random.choices(chars, k=10))
    # 更新資料庫密碼為新密碼
    update_password(email, hash_password(new_password))

    if await send_email(email, new_password):
        return f"已寄送密碼重設連結到 {email}。", "success", 200
    return "寄送失敗", "error", 500

def change_user_info_logic(user, payload: ModifyUserInfo):

    if user.email != payload.email and get_user_by_email(payload.email):
        return "此電子郵件已被其他帳戶使用", "error", 409

    if not payload.old_password:
        return "舊密碼為必填項目", "error", 400

    if payload.new_password:
        # 核對舊密碼是否正確
        if not verify_password(payload.old_password, user.password):
            return "舊密碼錯誤", "error", 401
        stored_password = hash_password(payload.new_password)
    else:
        stored_password = user.password

    # 更新 user 資訊
    if update_user_info(user.uid, payload.username, payload.email, stored_password):
        return "資料更新成功", "success", 200

    return "更新資料時發生錯誤", "error", 500

async def upload_user_photo_logic(photo, uid: int):
    content = await photo.read()
    # 格式檢查
    is_valid, reason = is_valid_image(photo, content)
    if not is_valid:
        return reason, "error", 400, None

    try:
        ext = photo.filename.rsplit(".", 1)[-1].lower()
        if ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
            return "不支援的檔案格式", "error", 400, None

        new_filename = f"{uuid.uuid4().hex}.{ext}"
        upload_folder = Path("user_photo")
        upload_folder.mkdir(parents=True, exist_ok=True)
        save_path = upload_folder / new_filename

        # 儲存新照片
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        user = get_user_by_uid(uid)
        if not user:
            return "找不到使用者", "error", 404, None

        old_img = user.img
        if not update_user_img(uid, new_filename):
            return "圖片更新失敗", "error", 500, None

        # 刪除舊照片
        if old_img:
            old_path = upload_folder / old_img
            if old_path.exists():
                old_path.unlink()

        return "大頭貼上傳成功", "success", 200, {"filename": new_filename}

    except Exception as e:
        print(f"[ERROR] 上傳大頭貼失敗：{e}")
        return "伺服器錯誤", "error", 500, None

def get_current_user_info_logic(uid: int):
    try:
        user = get_user_by_uid(uid)
        if not user:
            return "找不到使用者", "error", 404, None

        user_info = {
            "username": user.username,
            "email": user.email
        }
        return "取得使用者成功", "success", 200, {"user": user_info}

    except Exception as e:
        print(f"[ERROR] 取得使用者資料失敗：{e}")
        return "伺服器錯誤", "error", 500, None