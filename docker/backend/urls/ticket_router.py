from core.response import make_response
from dependencies import get_current_user, require_role
from fastapi import APIRouter, Depends, File, Path, Query, UploadFile
from schemas.ticket import TicketAuditRequest, TicketUpdate
from views.ticket import (audit_ticket_logic, change_ticket_logic,
                          delete_ticket_logic, list_class_logic,
                          list_date_logic, list_ticket_logic,
                          not_write_off_logic, search_ticket_logic,
                          total_money_logic, unaudited_invoices_logic,
                          upload_ticket_logic, write_off_logic)

ticket_router = APIRouter()

@ticket_router.get("/list", summary="查詢發票")
def list_ticket(current_user=Depends(get_current_user)):
    message, state, status_code, data = list_ticket_logic(current_user)
    return make_response(message, state, status_code, data)

@ticket_router.delete("/delete/{tid}", summary="刪除發票")
def delete_ticket(tid: int, current_user=Depends(get_current_user)):
    message, state, status_code = delete_ticket_logic(tid, current_user)
    return make_response(message, state, status_code)

@ticket_router.patch("/change/{tid}", summary="修改發票")
def change_ticket(
    tid: int,
    payload: TicketUpdate,
    current_user=Depends(get_current_user)
):
    message, state, status_code = change_ticket_logic(tid, payload, current_user)
    return make_response(message, state, status_code)

@ticket_router.get("/search", summary="查詢發票內容")
def search_ticket(q: str = Query(..., min_length=1), current_user=Depends(get_current_user)):
    message, state, status_code, data = search_ticket_logic(q.strip(), current_user)
    return make_response(message, state, status_code, data)

@ticket_router.post("/upload", summary="上傳發票圖片")
async def upload_ticket(
    photo: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    message, state, status_code, data = await upload_ticket_logic(photo, current_user)
    return make_response(message, state, status_code, data)

@ticket_router.get("/total_money", summary="總結金額")
def total_money(current_user=Depends(get_current_user)):
    message, state, status_code, data = total_money_logic(current_user)
    return make_response(message, state, status_code, data)

@ticket_router.get("/list_class", summary="查詢發票類別")
def list_class(current_user=Depends(get_current_user)):
    message, state, status_code, data = list_class_logic()
    return make_response(message, state, status_code, data)

@ticket_router.get("/list_date", summary="查詢發票日期")
def list_date(current_user=Depends(get_current_user)):
    message, state, status_code, data = list_date_logic()
    return make_response(message, state, status_code, data)

@ticket_router.get("/unaudited_invoices", summary="統計未審核發票數量")
def unaudited_invoices(current_user=Depends(get_current_user)):
    message, state, status_code, data = unaudited_invoices_logic()
    return make_response(message, state, status_code, data)

@ticket_router.get("/not_write_off", summary="統計未核銷發票總數")
def not_write_off(current_user=Depends(get_current_user)):
    message, state, status_code, data = not_write_off_logic()
    return make_response(message, state, status_code, data)

@ticket_router.get("/write_off", summary="統計已核銷發票與金額")
def write_off(current_user=Depends(get_current_user)):
    message, state, status_code, data = write_off_logic()
    return make_response(message, state, status_code, data)

@ticket_router.patch("/audit/{tid}", summary="審核發票")
def audit_ticket(
    tid: int = Path(..., description="欲審核的發票 ID"),
    payload: TicketAuditRequest = ...,
    current_user = Depends(require_role(1))  # 僅限管理員
):
    message, state, status_code = audit_ticket_logic(tid, payload.status)
    return make_response(message, state, status_code)