from typing import Tuple, List, Dict

from model.departments_model import (
    department_exists, create_department,
    delete_department_by_id, get_department_by_id,
    update_department_by_id, get_departments_budget_summary,
    get_department_accounts
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


def budget_summary_logic() -> Tuple[str, List[Dict]]:
    results = get_departments_budget_summary()
    if results is None:
        raise HTTPException(status_code=500, detail="查詢失敗")
    if not results:
        raise HTTPException(status_code=404, detail="查無資料")
    return "查詢成功", results


def department_accounts_logic(department_id: int) -> Tuple[str, List[Dict]]:
    results = get_department_accounts(department_id)
    if results is None:
        raise HTTPException(status_code=500, detail="查詢失敗")
    if not results:
        raise HTTPException(status_code=404, detail="查無資料")
    return "查詢成功", results