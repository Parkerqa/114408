from core.response import make_response
from dependencies import get_current_user
from fastapi import APIRouter, Depends
from schemas.setting import ColorSetting, ThemeUpdate
from views.settings import change_color_logic, change_theme_logic

setting_router = APIRouter()

@setting_router.patch("/change_theme", summary="修改黑白主題")
def change_theme(payload: ThemeUpdate, current_user=Depends(get_current_user)):
    message, state, status_code, data = change_theme_logic(current_user.uid, payload.theme)
    return make_response(message, state, status_code, data)

@setting_router.patch("/change_color", summary="更新顏色設定")
def change_color(payload: ColorSetting, current_user=Depends(get_current_user)):
    message, state, status_code = change_color_logic(current_user.uid, payload)
    return make_response(message, state, status_code)