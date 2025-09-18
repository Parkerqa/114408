from typing import Tuple, Dict
from model.setting_model import (update_or_insert_color_setting,
                                 update_or_insert_theme, get_user_color_setting)
from schemas.setting import ColorSetting
from starlette.exceptions import HTTPException


def change_theme_logic(user_id: int, theme: int):
    if theme not in (0, 1):
        raise HTTPException(status_code=400, detail="錯誤的主題參數")
    try:
        success = update_or_insert_theme(user_id, theme)
        if not success:
            raise HTTPException(status_code=500, detail="更新失敗")

        return "主題模式已更新", {"theme": theme}
    except Exception as e:
        print(f"[ERROR] 修改主題模式失敗：{e}")
        raise HTTPException(status_code=500, detail="修改主題模式失敗")


def change_color_logic(user_id: int, payload: ColorSetting) -> str:
    try:
        # 驗證邏輯條件
        if not (payload.red_usage_rate <= payload.red_remaining_rate and
                payload.yellow_usage_rate <= payload.yellow_remaining_rate and
                payload.green_usage_rate <= payload.green_remaining_rate):
            raise HTTPException(status_code=400, detail="bot 值不能大於 top")

        if not (payload.red_remaining_rate <= payload.yellow_usage_rate and
                payload.yellow_remaining_rate <= payload.green_usage_rate):
            raise HTTPException(status_code=400, detail="red 不可超過 yellow，yellow 不可超過 green")

        success = update_or_insert_color_setting(user_id, payload)
        if not success:
            raise HTTPException(status_code=500, detail="閾值更新失敗")

        return "閾值更新成功"

    except Exception as e:
        print(f"[ERROR] 更新 other_setting 閾值失敗：{e}")
        raise HTTPException(status_code=500, detail="閾值更新閾值失敗")


def get_color_logic(user_id: int) -> Tuple[str, Dict]:
    result = get_user_color_setting(user_id)
    if result is None:
        raise HTTPException(status_code=500, detail="讀取顏色設定失敗")

    return "取得顏色設定成功", result