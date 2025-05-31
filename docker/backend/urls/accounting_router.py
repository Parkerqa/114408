from core.response import make_response
from dependencies import get_current_user
from fastapi import APIRouter, Depends, Query
from views.accounting import list_accounting_logic

accounting_router = APIRouter()

@accounting_router.get("/list_accounting", summary="依種類查詢會計科目")
def list_accounting(class_: str = Query(..., alias="class"), current_user=Depends(get_current_user)):
    message, data = list_accounting_logic(class_)
    return make_response(message, data=data)