from core.response import make_response
from dependencies import get_current_user
from fastapi import APIRouter, Depends
from schemas.departments import DepartmentCreate, DepartmentUpdate
from views.departments import (add_department_logic, delete_department_logic,
                               update_department_logic)

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