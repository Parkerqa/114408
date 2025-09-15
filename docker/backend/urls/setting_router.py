from core.response import make_response
from dependencies import get_current_user
from fastapi import APIRouter, Depends
from schemas.setting import ColorSetting, ThemeUpdate
from views.setting import change_color_logic, change_theme_logic, get_color_logic

setting_router = APIRouter()


@setting_router.patch("/change_theme", summary="修改黑白主題")
def change_theme(payload: ThemeUpdate, current_user=Depends(get_current_user)):
    message, data = change_theme_logic(current_user.user_id, payload.theme)
    return make_response(message, data=data)


@setting_router.patch("/change_color", summary="更新顏色設定")
def change_color(payload: ColorSetting, current_user=Depends(get_current_user)):
    message = change_color_logic(current_user.user_id, payload)
    return make_response(message)


@setting_router.get("/get_color", summary="取得顏色設定")
def get_color(current_user=Depends(get_current_user)):
    message, data = get_color_logic(current_user.user_id)
    return make_response(message, data=data)