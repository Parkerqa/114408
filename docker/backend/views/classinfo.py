from model.classinfo_model import (class_exists, create_class,
                                   delete_class_by_id, get_class_by_id,
                                   update_class_by_id)
from schemas.classinfo import ClassCreate
from starlette.exceptions import HTTPException


def add_class_logic(payload: ClassCreate) -> str:
    try:
        if class_exists(payload.class_):
            raise HTTPException(status_code=409, detail="類別名稱已存在，請使用不同名稱")

        if not create_class(payload.class_, payload.money_limit):
            raise HTTPException(status_code=500, detail="新增失敗")

        return "新增成功"

    except Exception as e:
        print(f"[ERROR] 新增 class 發生錯誤：{e}")
        raise HTTPException(status_code=500, detail="新增 class 發生錯誤")


def update_class_logic(cid: int, payload) -> str:
    try:
        existing = get_class_by_id(cid)
        if not existing:
            raise HTTPException(status_code=404, detail="找不到該筆資料")

        success = update_class_by_id(cid, payload.class_, payload.money_limit)
        if not success:
            raise HTTPException(status_code=500, detail="更新失敗")

        return "更新成功"

    except Exception as e:
        print(f"[ERROR] 更新 class 發生錯誤：{e}")
        raise HTTPException(status_code=500, detail="伺服器錯誤")


def delete_class_logic(cid: int) -> str:
    try:
        existing = get_class_by_id(cid)
        if not existing:
            raise HTTPException(status_code=404, detail="找不到該筆資料")

        if not delete_class_by_id(cid):
            raise HTTPException(status_code=500, detail="刪除失敗")

        return "刪除成功"

    except Exception as e:
        print(f"[ERROR] 刪除 class 發生錯誤：{e}")
        raise HTTPException(status_code=500, detail="刪除 class 發生錯誤")
