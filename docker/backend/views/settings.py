from model.setting_model import (update_or_insert_color_setting,
                                 update_or_insert_theme)


def change_theme_logic(uid: int, theme: int):
    if theme not in (0, 1):
        return "錯誤的主題參數", "error", 400, None
    try:
        success = update_or_insert_theme(uid, theme)
        if not success:
            return "更新失敗", "error", 500, None

        return "主題模式已更新", "success", 200, {"theme": theme}
    except Exception as e:
        print(f"[ERROR] 修改主題模式失敗：{e}")
        return "伺服器錯誤", "error", 500, None

def change_color_logic(uid: int, payload):
    try:
        # 驗證邏輯條件
        if not (payload.red_but <= payload.red_top and
                payload.yellow_but <= payload.yellow_top and
                payload.green_but <= payload.green_top):
            return "but 值不能大於 top", "error", 400

        if not (payload.red_top <= payload.yellow_but and
                payload.yellow_top <= payload.green_but):
            return "red 不可超過 yellow，yellow 不可超過 green", "error", 400

        success = update_or_insert_color_setting(uid, payload)
        if not success:
            return "更新失敗", "error", 500

        return "閾值更新成功", "success", 200

    except Exception as e:
        print(f"[ERROR] 更新 other_setting 閾值失敗：{e}")
        return "伺服器錯誤", "error", 500