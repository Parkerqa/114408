import os
from typing import Dict, List, Optional, Tuple, Any

from core.upload_utils import upload_image
from fastapi import UploadFile
from model.ticket_model import (count_by_status, count_status_1, create_ticket,
                                create_ticket_detail, delete_ticket_by_id,
                                delete_ticket_details_by_ids, get_all_tickets,
                                get_detail_ids_by_tid, get_specify_ticket, get_tickets_by_ids,
                                get_ticket_by_id, get_tickets_by_user,
                                get_total_money, search_tickets_combined,
                                sum_money_by_status, update_ticket_class,
                                update_ticket_detail, bulk_update_ticket_status,
                                get_latest_approved, get_pending_reimbursements,
                                get_approved_records, update_ticket_info)
from schemas.ticket import TicketAuditBulkRequest, TicketList, TicketOut
from starlette.exceptions import HTTPException
from datetime import date

from views.checker import check_mode, check_status, check_type


def list_ticket_logic(mode, user) -> Tuple[str, List[Dict] or None]:
    user_id = user.user_id
    priority = user.priority

    if priority in (0, 3):
        tickets = get_all_tickets(check_mode(mode))
    else:
        tickets = get_tickets_by_user(user_id, check_mode(mode))

    if not tickets:
        return "目前沒有發票資料", None

    results = []
    for t in tickets:
        is_processing = t.status == 1

        if not is_processing:
            details = [
                {"title": detail.title, "money": str(int(detail.money)) if detail.money is not None else "0"}
                for detail in t.ticket_detail if detail.title
            ]
            if not details:
                details = [] if t.status != 0 else [{"title": check_status(t.status), "money": "0"}]
        else:
            details = []

        result = {
            "id": t.ticket_id,
            "time": t.created_at.strftime("%Y-%m-%d"),
            "type": check_type(t.type) if not is_processing else "等待系統辨識",
            "Details": details if not is_processing else [],
            "invoice_number": t.invoice_number if not is_processing and t.invoice_number is not None else (
                check_status(t.status) if t.status == 0 else "等待系統辨識"),
            "total_money": str(int(t.total_money)) if not is_processing and t.total_money is not None else (
                check_status(t.status) if t.status == 0 else "等待系統辨識"
            ),
            "status": check_status(t.status)
        }
        results.append(result)

    return "成功", results


def list_specify_ticket_logic(ticket_id: int, user) -> Tuple[str, Dict or None]:
    ticket = get_specify_ticket(user.user_id, ticket_id)

    if not ticket:
        raise HTTPException(status_code=403, detail="你無權查詢此發票")

    is_processing = ticket.status == 1

    if not is_processing:
        details = [
            {
                "td_id": detail.td_id,
                "title": detail.title,
                "money": str(int(detail.money)) if detail.money is not None else "0"
            }
            for detail in ticket.ticket_detail if detail.title
        ]
        if not details:
            details = [] if ticket.status != 0 else [
                {"td_id": None, "title": check_status(ticket.status), "money": "0"}
            ]
    else:
        details = []

    result = {
        "id": ticket.ticket_id,
        "time": ticket.created_at.strftime("%Y-%m-%d"),
        "type": check_type(ticket.type) if not is_processing else "等待系統辨識",
        "Details": details if not is_processing else [],
        "invoice_number": ticket.invoice_number if not is_processing and ticket.invoice_number is not None else (
            check_status(ticket.status) if ticket.status == 0 else "等待系統辨識"),
        "total_money": str(int(ticket.total_money)) if not is_processing and ticket.total_money is not None else (
            check_status(ticket.status) if ticket.status == 0 else "等待系統辨識"
        ),
        "status": check_status(ticket.status)
    }

    return "查詢成功", result


def list_multi_tickets_logic(payload: TicketList) -> Tuple[str, List[Dict]]:
    try:
        ticket_ids = payload.ticket_id
        if not ticket_ids:
            raise HTTPException(status_code=400, detail="ticket_id 不可為空")

        tickets = get_tickets_by_ids(ticket_ids)
        if tickets is None:
            raise HTTPException(status_code=500, detail="查詢失敗")
        if not tickets:
            return "查詢成功", None

        results = []
        for ticket in tickets:
            is_processing = ticket.status == 1

            # 處理明細 (ticket_detail)
            details = []
            if ticket.ticket_detail:
                details = [
                    {
                        "title": d.title,
                        "money": float(d.money) if d.money is not None else 0.0
                    }
                    for d in ticket.ticket_detail if d.title
                ]

            applicant = ticket.user.username if ticket.user else ticket.created_by

            result = {
                "ticket_id": ticket.ticket_id,
                "Details": details if not is_processing else [],
                "time": ticket.created_at.strftime("%Y/%m/%d") if ticket.created_at else None,
                "type": check_type(ticket.type) if not is_processing else "等待系統辨識",
                "applicant": applicant if not is_processing else "等待系統辨識",
                "img_url": f'{os.getenv("BASE_INVOICE_IMAGE_URL")}{ticket.img}' if ticket.img else None,
            }
            results.append(result)

        return "查詢成功", results

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] list_multi_tickets_logic failed: {e}")
        raise HTTPException(status_code=500, detail="伺服器錯誤")


def delete_ticket_logic(ticket_id: int, user) -> str:
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="找不到該發票")

    # status 為 3 表示發票已完成，禁止任何人刪除
    if ticket.status == 3:
        raise HTTPException(status_code=403, detail="無法刪除已完成的發票")

    # 一般使用者只能刪除自己的發票
    if user.priority == 1 and ticket.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="你無權刪除此發票")

    success = delete_ticket_by_id(ticket_id)
    if success:
        return "發票已成功刪除"
    raise HTTPException(status_code=500, detail="刪除發票時發生錯誤")


def change_ticket_logic(ticket_id: int, payload, user) -> str:
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="找不到發票")

    if ticket.status == 3:
        raise HTTPException(status_code=403, detail="無法修改已完成的發票")

    if user.priority == 0 and ticket.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="你無權修改這張發票")

    # 更新基本資訊 + total_money
    success = update_ticket_info(ticket_id, payload.type, payload.invoice_number, payload.total_money)
    if not success:
        raise HTTPException(status_code=500, detail="更新發票資訊失敗")

    # 明細處理（跟原本一樣）
    existing_ids = set(get_detail_ids_by_tid(ticket_id))
    new_ids = set()

    for item in payload.Details:
        if item.title is None or item.money is None:
            continue

        if item.td_id:
            if item.td_id in existing_ids:
                success = update_ticket_detail(item.td_id, ticket_id, item.title, item.money)
                if not success:
                    raise HTTPException(status_code=500, detail=f"更新明細 ID {item.td_id} 失敗")
                new_ids.add(item.td_id)
            else:
                raise HTTPException(status_code=404, detail=f"找不到明細 id {item.td_id}")
        else:
            success = create_ticket_detail(ticket_id, item.title, item.money)
            if not success:
                raise HTTPException(status_code=500, detail="新增明細失敗")

    ids_to_delete = existing_ids - new_ids
    if ids_to_delete:
        success = delete_ticket_details_by_ids(ids_to_delete)
        if not success:
            raise HTTPException(status_code=500, detail="刪除舊明細失敗")

    return "發票已成功修改"


def search_ticket_logic(
    status: List[int],
    keyword: Optional[str],
    date: Optional[date],
    limit: int,
    user,
):
    tickets = search_tickets_combined(
        status=status,
        keyword=keyword,
        date=date,
        limit=limit,
    )

    if tickets is None:
        raise HTTPException(status_code=500, detail="查詢發生錯誤")

    if not tickets:
        raise HTTPException(status_code=404, detail="查無資料")

    # 如果 user.priority == 0 → 過濾自己的
    if user.priority == 0:
        tickets = [t for t in tickets if t.user_id == user.user_id]

    if not tickets:
        raise HTTPException(status_code=403, detail="沒有權限查看這些資料")

    results = []
    for t in tickets:
        results.append({
            "id": t.ticket_id,
            "time": t.created_at.strftime("%Y-%m-%d") if t.created_at else None,
            "type": check_type(t.type),
            "invoice_number": t.invoice_number,
            "total_money": int(t.total_money),
            "status": check_status(t.status),
            "Details": [
                {
                    "id": d.td_id,
                    "title": d.title,
                    "money": int(d.money) if d.money is not None else 0
                }
                for d in t.ticket_detail
            ]
        })

    return "查詢成功", results


async def upload_ticket_logic(image: UploadFile, user) -> Tuple[str, List[Dict] or None]:
    img_bytes = await image.read()
    new_filename = upload_image(image, img_bytes, 1)

    # 建立發票資料
    ticket_id = create_ticket(user.user_id, new_filename)

    if not ticket_id:
        raise HTTPException(status_code=500, detail="建立發票失敗")

    return "圖片上傳並建立新發票成功", {
        "filename": new_filename,
        "ticket_id": ticket_id
    }


def total_money_logic(user) -> Tuple[str, List[Dict] or None]:
    try:
        total = get_total_money(user)
        return "查詢成功", {"total_money": total}
    except Exception as e:
        print(f"[ERROR] 加總 money 失敗：{e}")
        raise HTTPException(status_code=500, detail="加總時發生錯誤")


def unaudited_invoices_logic() -> Tuple[str, List[Dict] or None]:
    try:
        count = count_status_1()
        return "統計成功", {"status_1_count": count}
    except Exception as e:
        print(f"[ERROR] 統計 status=1 錯誤：{e}")
        raise HTTPException(status_code=500, detail="統計失敗")


def not_write_off_logic() -> Tuple[str, List[Dict] or None]:
    try:
        count_0 = count_by_status(0)
        count_1 = count_by_status(1)
        total = count_0 + count_1

        return "統計成功", {"total": total}
    except Exception as e:
        print(f"[ERROR] 統計 Ticket status 錯誤：{e}")
        raise HTTPException(status_code=500, detail="統計失敗")


def write_off_logic() -> Tuple[str, List[Dict] or None]:
    try:
        count = count_by_status(2)
        total_money = sum_money_by_status(2)

        return "統計成功", {
            "count": count,
            "total_money": total_money
        }
    except Exception as e:
        print(f"[ERROR] 統計 status=2 與金額加總錯誤：{e}")
        raise HTTPException(status_code=500, detail="統計失敗")


def audit_ticket_bulk_logic(payload: TicketAuditBulkRequest, user) -> Tuple[str, Dict[str, Any]]:
    try:
        result = bulk_update_ticket_status(payload, checker_user_id=user.user_id)
        return "批次審核完成", result
    except Exception as e:
        print(f"[ERROR] audit_ticket_bulk_logic: {e}")
        raise HTTPException(status_code=500, detail="批次審核時發生錯誤")


def list_latest_approved_logic(limit: int = 4):
    rows = get_latest_approved(limit=limit)
    if rows is None:
        raise HTTPException(status_code=500, detail="查詢失敗")
    return "最新過審資料查詢成功", rows


def list_pending_reimbursements_logic(limit: int = 20):
    rows = get_pending_reimbursements(limit=limit)
    if rows is None:
        raise HTTPException(status_code=500, detail="查詢失敗")
    return "待核銷申請查詢成功", rows


def list_approved_records_logic(limit: int = 20):
    rows = get_approved_records(limit=limit)
    if rows is None:
        raise HTTPException(status_code=500, detail="查詢失敗")
    return "已核銷資料查詢成功", rows
