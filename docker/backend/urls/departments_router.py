from core.response import make_response
from dependencies import get_current_user, require_role
from fastapi import APIRouter, Depends, Path
from schemas.departments import DepartmentCreate, DepartmentUpdate, DepartmentAccountingSync
from views.departments import (add_department_logic, delete_department_logic,
                               update_department_logic, budget_summary_logic,
                               department_accounts_logic, get_departments_with_accounts_logic,
                               sync_department_accounting_logic)

departments_router = APIRouter()


@departments_router.post("/add", summary="新增部門")
def add_department(payload: DepartmentCreate, current_user=Depends(require_role(0, 3))):
    message = add_department_logic(payload)
    return make_response(message)


@departments_router.patch("/update/{dept_id}", summary="修改部門")
def update_department(dept_id: int, payload: DepartmentUpdate, current_user=Depends(require_role(0, 3))):
    message = update_department_logic(dept_id, payload)
    return make_response(message)


@departments_router.delete("/delete/{dept_id}", summary="刪除部門")
def delete_department(dept_id: int, current_user=Depends(require_role(0, 3))):
    message = delete_department_logic(dept_id)
    return make_response(message)


@departments_router.get("/budget_summary", summary="各部門總預算")
def budget_summary(current_user=Depends(require_role(0, 3))):
    message, data = budget_summary_logic()
    return make_response(message, data=data)


@departments_router.get("/{department_id}/show_accounts", summary="部門會計科目與預算")
def department_accounts(
    department_id: int = Path(..., description="部門 ID"),
    current_user=Depends(require_role(0, 3))
):
    message, data = department_accounts_logic(department_id)
    return make_response(message, data=data)


@departments_router.get("/with_accounts", summary="取得部門與對應會計科目")
def departments_with_accounts(current_user=Depends(require_role(0, 3))):
    message, data = get_departments_with_accounts_logic()
    return make_response(message, data=data)


@departments_router.put(
    "/{department_id}/accountings",
    summary="同步更新部門底下的會計科目與預算（新增、更新、刪除）"
)
def sync_department_accountings(
    department_id: int = Path(..., description="部門 ID"),
    payload: DepartmentAccountingSync = ...,
    current_user=Depends(require_role(0, 3))
):
    message = sync_department_accounting_logic(department_id, payload, current_user)
    return make_response(message)