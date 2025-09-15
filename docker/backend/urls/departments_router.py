from core.response import make_response
from dependencies import get_current_user
from fastapi import APIRouter, Depends, Path
from schemas.departments import DepartmentCreate, DepartmentUpdate
from views.departments import (add_department_logic, delete_department_logic,
                               update_department_logic, budget_summary_logic,
                               department_accounts_logic)

departments_router = APIRouter()


@departments_router.post("/add", summary="新增部門")
def add_department(payload: DepartmentCreate, current_user=Depends(get_current_user)):
    message = add_department_logic(payload)
    return make_response(message)


@departments_router.patch("/update/{dept_id}", summary="修改部門")
def update_department(dept_id: int, payload: DepartmentUpdate, current_user=Depends(get_current_user)):
    message = update_department_logic(dept_id, payload)
    return make_response(message)


@departments_router.delete("/delete/{dept_id}", summary="刪除部門")
def delete_department(dept_id: int, current_user=Depends(get_current_user)):
    message = delete_department_logic(dept_id)
    return make_response(message)


@departments_router.get("/budget_summary", summary="各部門總預算")
def budget_summary(current_user=Depends(get_current_user)):
    message, data = budget_summary_logic()
    return make_response(message, data=data)


@departments_router.get("/{department_id}/accounts", summary="部門會計科目與預算")
def department_accounts(
    department_id: int = Path(..., description="部門 ID"),
    current_user=Depends(get_current_user)
):
    message, data = department_accounts_logic(department_id)
    return make_response(message, data=data)