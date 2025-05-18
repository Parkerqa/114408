from core.response import make_response
from dependencies import require_role
from fastapi import APIRouter, Depends, File, UploadFile
from schemas.user import ModifyUserInfo, PasswordForget, UserCreate, UserLogin
from views.user import (change_user_info_logic, forget_password_logic,
                        get_current_user_info_logic,
                        get_current_user_settings_logic, login_logic,
                        register_logic, upload_user_photo_logic)

user_router = APIRouter()

@user_router.post("/register", summary="註冊")
def register(payload: UserCreate):
    message, state, status_code= register_logic(payload)
    return make_response(message, state, status_code)

@user_router.post("/login", summary="登入")
def login(payload: UserLogin):
    message, state, status_code, data = login_logic(payload)
    return make_response(message, state, status_code, data)

@user_router.post("/forget_password", summary="忘記密碼")
async def forget_password(payload: PasswordForget):
    message, state, status_code = await forget_password_logic(payload.email)
    return make_response(message, state, status_code)

@user_router.patch("/change_user_info", summary="修改使用者資料")
def change_user_info(
    payload: ModifyUserInfo,
    current_user=Depends(require_role(0, 1))
):
    message, state, status_code = change_user_info_logic(current_user, payload)
    return make_response(message, state, status_code)

@user_router.post("/upload_user_photo", summary="上傳使用者大頭貼")
async def upload_user_photo(
    photo: UploadFile = File(...),
    current_user=Depends(require_role(0, 1))
):
    message, state, status_code, data = await upload_user_photo_logic(photo, current_user.uid)
    return make_response(message, state, status_code, data)

@user_router.get("/me", summary="取得當前使用者資料")
def get_current_user_info(current_user=Depends(require_role(0, 1))):
    message, state, status_code, data = get_current_user_info_logic(current_user.uid)
    return make_response(message, state, status_code, data)

@user_router.get("/me_config", summary="取得當前使用者設定檔")
def get_current_user_settings(current_user=Depends(require_role(0, 1))):
    message, state, status_code, data = get_current_user_settings_logic(current_user.uid)
    return make_response(message, state, status_code, data)