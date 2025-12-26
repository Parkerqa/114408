from typing import Optional, List, Union

from core.response import make_response
from dependencies import get_current_user, require_role
from fastapi import (APIRouter, BackgroundTasks, Depends, File, Path, Query,
                     UploadFile)
from fastapi.encoders import jsonable_encoder
from datetime import date

from schemas.ticket import TicketAuditBulkRequest, TicketUpdate, TicketList, TicketOut
from views.parser import invoice_parser
from views.ticket import (audit_ticket_bulk_logic, change_ticket_logic,
                          delete_ticket_logic, list_specify_ticket_logic, list_multi_tickets_logic,
                          list_ticket_logic, not_write_off_logic,
                          search_ticket_logic, total_money_logic,
                          unaudited_invoices_logic, upload_ticket_logic,
                          write_off_logic, list_latest_approved_logic,
                          list_pending_reimbursements_logic, list_approved_records_logic,
                          get_ticket_report_logic)

ticket_router = APIRouter()


@ticket_router.get("/list", summary="列出發票")
def list_ticket(mode: Optional[int] = Query(None, ge=0, le=1), current_user=Depends(get_current_user)):
    message, data = list_ticket_logic(mode, current_user)
    return make_response(message, data=data)


@ticket_router.get("/list/{ticket_id}", summary="查詢單筆發票")
def list_specify_ticket(ticket_id: int, current_user=Depends(get_current_user)):
    message, data = list_specify_ticket_logic(ticket_id, current_user)
    return make_response(message, data=data)


@ticket_router.post("/multi_list", summary="查詢多筆發票")
def list_multi_ticket(payload: TicketList, current_user=Depends(require_role(0))):
    message, data = list_multi_tickets_logic(payload)
    return make_response(message, data=data)


@ticket_router.delete("/delete/{ticket_id}", summary="刪除發票")
def delete_ticket(ticket_id: int, current_user=Depends(get_current_user)):
    message = delete_ticket_logic(ticket_id, current_user)
    return make_response(message)


@ticket_router.patch("/change/{ticket_id}", summary="修改發票")
def change_ticket(
        ticket_id: int,
        payload: TicketUpdate,
        current_user=Depends(get_current_user)
):
    message = change_ticket_logic(ticket_id, payload, current_user)
    return make_response(message)


@ticket_router.get("/search", summary="核銷報帳合併查詢（status 必填，關鍵字 / 類別 / 日期為選填）", response_model=List[TicketOut])
def search_ticket(
    status: Union[List[int], str] = Query(..., description="發票狀態（可傳多個）"),
    q: Optional[str] = Query(None, min_length=1),
    date: Optional[date] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    current_user=Depends(require_role(0)),
):
    if isinstance(status, str):
        status = [int(s) for s in status.split(",") if s.strip()]

    message, tickets_out = search_ticket_logic(
        status=status,
        keyword=q.strip() if q else None,
        date=date,
        limit=limit,
        user=current_user,
    )

    data = jsonable_encoder(tickets_out)

    return make_response(message, data=data)


@ticket_router.post("/upload", summary="上傳發票圖片")
async def upload_ticket(
        background_tasks: BackgroundTasks,
        photo: UploadFile = File(...),
        current_user=Depends(get_current_user),
):
    message, data = await upload_ticket_logic(photo, current_user)
    background_tasks.add_task(invoice_parser, data["filename"], data["ticket_id"])
    return make_response(message, data=data)


@ticket_router.get("/total_money", summary="總結金額")
def total_money(current_user=Depends(get_current_user)):
    message, data = total_money_logic(current_user)
    return make_response(message, data=data)


@ticket_router.get("/unaudited_invoices", summary="統計未審核發票數量")
def unaudited_invoices(current_user=Depends(get_current_user)):
    message, data = unaudited_invoices_logic()
    return make_response(message, data=data)


@ticket_router.get("/not_write_off", summary="統計未核銷發票總數")
def not_write_off(current_user=Depends(get_current_user)):
    message, data = not_write_off_logic()
    return make_response(message, data=data)


@ticket_router.get("/write_off", summary="統計已核銷發票與金額")
def write_off(current_user=Depends(get_current_user)):
    message, data = write_off_logic()
    return make_response(message, data=data)


@ticket_router.patch("/audit", summary="批次審核發票（每筆可不同狀態）")
def audit_ticket_bulk(
    payload: TicketAuditBulkRequest,
    current_user=Depends(require_role(0, 2, 3)),
):
    message, data = audit_ticket_bulk_logic(payload, current_user)
    return make_response(message, data=data)


@ticket_router.get("/latest_approved", summary="最新過審的4筆資料")
def latest_approved(limit: int = Query(4, ge=1, le=50), current_user=Depends(require_role(0))):
    message, data = list_latest_approved_logic(limit=limit)
    return make_response(message, data=data)


@ticket_router.get("/pending_reimbursements", summary="代核銷的申請（待審中）")
def list_pending_reimbursements(
    limit: int = Query(20, ge=1, le=100),
    current_user=Depends(require_role(0)),
):
    message, data = list_pending_reimbursements_logic(limit=limit)
    return make_response(message, data=data)


@ticket_router.get("/approved_records", summary="已核銷的資料紀錄")
def list_approved_records(
    limit: int = Query(20, ge=1, le=100),
    current_user=Depends(require_role(0)),
):
    message, data = list_approved_records_logic(limit=limit)
    return make_response(message, data=data)


@ticket_router.get("/report", summary="依日期區間查詢核銷報帳資訊")
def get_ticket_report(
    start_date: date = Query(..., description="開始日期 yyyy-mm-dd"),
    end_date: date = Query(..., description="結束日期 yyyy-mm-dd"),
    current_user=Depends(get_current_user)
):
    message, data = get_ticket_report_logic(start_date, end_date, current_user)
    return make_response(message, data=data)