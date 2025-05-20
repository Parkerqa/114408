from model.classinfo_model import (class_exists, create_class,
                                   delete_class_by_id, get_class_by_id,
                                   update_class_by_id)
from schemas.classinfo import ClassCreate


def add_class_logic(payload: ClassCreate):
    try:
        if class_exists(payload.class_):
            return "類別名稱已存在，請使用不同名稱", "error", 409

        if not create_class(payload.class_, payload.money_limit):
            return "新增失敗", "error", 500

        return "新增成功", "success", 201

    except Exception as e:
        print(f"[ERROR] 新增 class 發生錯誤：{e}")
        return "伺服器錯誤", "error", 500

def update_class_logic(cid: int, payload):
    try:
        existing = get_class_by_id(cid)
        if not existing:
            return "找不到該筆資料", "error", 404

        success = update_class_by_id(cid, payload.class_, payload.money_limit)
        if not success:
            return "更新失敗", "error", 500

        return "更新成功", "success", 200

    except Exception as e:
        print(f"[ERROR] 更新 class 發生錯誤：{e}")
        return "伺服器錯誤", "error", 500

def delete_class_logic(cid: int):
    try:
        existing = get_class_by_id(cid)
        if not existing:
            return "找不到該筆資料", "error", 404

        if not delete_class_by_id(cid):
            return "刪除失敗", "error", 500

        return "刪除成功", "success", 200

    except Exception as e:
        print(f"[ERROR] 刪除 class 發生錯誤：{e}")
        return "伺服器錯誤", "error", 500


