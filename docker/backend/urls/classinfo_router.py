from core.response import make_response
from dependencies import get_current_user
from fastapi import APIRouter, Depends
from schemas.classinfo import ClassCreate, ClassUpdate
from views.classinfo import (add_class_logic, delete_class_logic,
                             update_class_logic)

classinfo_router = APIRouter()

@classinfo_router.post("/add_class", summary="新增類別")
def add_class(payload: ClassCreate, current_user=Depends(get_current_user)):
    message, state, status_code = add_class_logic(payload)
    return make_response(message, state, status_code)

@classinfo_router.patch("/change_class/{cid}", summary="修改類別")
def update_class(cid: int, payload: ClassUpdate, current_user=Depends(get_current_user)):
    message, state, status_code = update_class_logic(cid, payload)
    return make_response(message, state, status_code)

@classinfo_router.delete("/delete_class/{cid}", summary="刪除類別")
def delete_class(cid: int, current_user=Depends(get_current_user)):
    message, state, status_code = delete_class_logic(cid)
    return make_response(message, state, status_code)

