from model.departments_model import (
    department_exists, create_department,
    delete_department_by_id, get_department_by_id,
    update_department_by_id
)
from schemas.departments import DepartmentCreate
from starlette.exceptions import HTTPException


def add_department_logic(payload: DepartmentCreate) -> str:
    try:
        if department_exists(payload.name):
            raise HTTPException(status_code=409, detail="部門名稱已存在，請使用不同名稱")

        if not create_department(payload.name, payload.money_limit):
            raise HTTPException(status_code=500, detail="新增失敗")

        return "新增成功"
    except Exception as e:
        print(f"[ERROR] 新增 department 發生錯誤：{e}")
        raise HTTPException(status_code=500, detail="新增 department 發生錯誤")


def update_department_logic(dept_id: int, payload) -> str:
    try:
        existing = get_department_by_id(dept_id)
        if not existing:
            raise HTTPException(status_code=404, detail="找不到該筆資料")

        success = update_department_by_id(dept_id, payload.name, payload.money_limit)
        if not success:
            raise HTTPException(status_code=500, detail="更新失敗")

        return "更新成功"
    except Exception as e:
        print(f"[ERROR] 更新 department 發生錯誤：{e}")
        raise HTTPException(status_code=500, detail="伺服器錯誤")


def delete_department_logic(dept_id: int) -> str:
    try:
        existing = get_department_by_id(dept_id)
        if not existing:
            raise HTTPException(status_code=404, detail="找不到該筆資料")

        if not delete_department_by_id(dept_id):
            raise HTTPException(status_code=500, detail="刪除失敗")

        return "刪除成功"
    except Exception as e:
        print(f"[ERROR] 刪除 department 發生錯誤：{e}")
        raise HTTPException(status_code=500, detail="刪除 department 發生錯誤")