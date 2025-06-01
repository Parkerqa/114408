from typing import Dict, List, Tuple

from core.upload_utils import upload_image
from fastapi import UploadFile
from model.ticket_model import (count_by_status, count_status_1, create_ticket,
                                create_ticket_detail, delete_ticket_by_id,
                                delete_ticket_details_by_ids, get_all_tickets,
                                get_detail_ids_by_tid, get_distinct_classes,
                                get_distinct_dates, get_ticket_by_id,
                                get_tickets_by_user, get_total_money,
                                search_tickets_by_keyword, sum_money_by_status,
                                update_ticket_class, update_ticket_detail,
                                update_ticket_status)
from starlette.exceptions import HTTPException

def check_type(type: str) -> str:
    if type == 0:
        return "系統辨識失敗"
    elif type == 1:
        return "等待系統辨識"
    elif type == 2:
        return "傳統發票"
    elif type == 3:
        return "電子發票"
    elif type == 4:
        return "二聯發票"
    elif type == 5:
        return "三聯發票"
    elif type == 6:
        return "收據"

def check_status(status: int) -> str:
    if status == 0:
        return "系統辨識失敗"
    elif status == 1:
        return "等待系統辨識"
    elif status == 2:
        return "待審核"
    elif status == 3:
        return "審核通過"
    elif status == 4:
        return "審核未通過"


def list_ticket_logic(user) -> Tuple[str, List[Dict] or None]:
    user_id = user.user_id
    priority = user.priority

    if priority == 1:
        tickets = get_all_tickets()
    else:
        tickets = get_tickets_by_user(user_id)

    if not tickets:
        return "目前沒有發票資料", None

    results = []
    # 處理結果格式
    for t in tickets:
        is_processing = t.status == 1

        if not is_processing:
            # 串接所有對應的 TicketDetail.title
            titles = [detail.title for detail in t.ticket_details if detail.title]
            title_text = ", ".join(titles) if titles else (
                check_status(t.status) if t.status == 0 else "無品項")

        result = {
            "time": t.create_date.strftime("%Y-%m-%d"),
            "type": check_type(t.type) if not is_processing else "等待系統辨識",
            "title": title_text if not is_processing else "等待系統辨識",
            "invoice_number": t.invoice_number if not is_processing and t.invoice_number is not None else (
                check_status(t.status) if t.status == 0 else "等待系統辨識"),
            "money": str(int(t.total_money)) if not is_processing and t.total_money is not None else (
                check_status(t.status) if t.status == 0 else "等待系統辨識"
                ),
            "state": check_status(t.status)
        }
        results.append(result)

    return "成功", results

def delete_ticket_logic(ticket_id: int, user) -> str:
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="找不到該發票")

    # status 為 2 表示發票已完成，禁止任何人刪除
    if ticket.status == 2:
        raise HTTPException(status_code=403, detail="無法刪除已完成的發票")

    # 一般使用者只能刪除自己的發票
    if user.priority == 0 and ticket.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="你無權刪除此發票")

    success = delete_ticket_by_id(ticket_id)
    if success:
        return "發票已成功刪除"
    raise HTTPException(status_code=500, detail="刪除發票時發生錯誤")

def change_ticket_logic(ticket_id: int, payload, user) -> str:
    if not payload.class_ or not isinstance(payload.detail, list):
        raise HTTPException(status_code=400, detail="請提供 class 和 detail")

    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="找不到發票")

    if ticket.status == 2:
        raise HTTPException(status_code=403, detail="無法修改已完成的發票")

    if user.priority == 0 and ticket.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="你無權修改這張發票")

    if not update_ticket_class(ticket_id, payload.class_):
        raise HTTPException(status_code=500, detail="更新主分類失敗")

    existing_ids = set(get_detail_ids_by_tid(ticket_id))
    new_ids = set()

    for item in payload.detail:
        if item.title is None or item.money is None:
            continue

        if item.id:
            if item.id in existing_ids:
                success = update_ticket_detail(item.id, ticket_id, item.title, item.money)
                if not success:
                    raise HTTPException(status_code=500, detail=f"更新明細 ID {item.id} 失敗")
                new_ids.add(item.id)
            else:
                raise HTTPException(status_code=404, detail=f"找不到明細 id {item.id}")
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

def search_ticket_logic(keyword: str, user) -> Tuple[str, List[Dict] or None]:
    tickets = search_tickets_by_keyword(keyword)

    if not tickets:
        raise HTTPException(status_code=404, detail="查無資料")

    filtered = []

    for row in tickets:
        if user.priority == 0:
            # 一般使用者只能看到自己的票
            if row.user_id != user.user_id:
                continue
            filtered.append({
                "class": row.class_,
                "ticket_create": row.createdate,
                "invoice_number": row.invoice_number,
                "title": row.title,
                "money": row.money
            })
        else:
            # 管理員：可看所有欄位
            filtered.append({
                "ticket_id": row.ticket_id,
                "class": row.class_,
                "user_id": row.user_id,
                "status": row.status,
                "invoice_number": row.invoice_number,
                "createdate": row.createdate,
                "title": row.title,
                "money": row.money
            })

    return "查詢成功", filtered

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

def list_class_logic() -> Tuple[str, List[Dict] or None]:
    try:
        classes = get_distinct_classes()
        return "查詢成功", {"classes": classes}
    except Exception as e:
        print(f"[ERROR] 查詢類別失敗：{e}")
        raise HTTPException(status_code=500, detail="查詢類別時發生錯誤")

def list_date_logic() -> Tuple[str,  List[Dict] or None]:
    try:
        dates = get_distinct_dates()
        return "查詢成功", {"dates": dates}
    except Exception as e:
        print(f"[ERROR] 查詢日期失敗：{e}")
        raise HTTPException(status_code=500, detail="查詢日期時發生錯誤")

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

def audit_ticket_logic(ticket_id: int, status: int):
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="找不到該發票")

    if ticket.status == 2:
        raise HTTPException(status_code=400, detail="該發票已完成，無法重新審核")

    if update_ticket_status(ticket_id, status):
        return "審核成功"

    raise HTTPException(status_code=500, detail="更新資料失敗")