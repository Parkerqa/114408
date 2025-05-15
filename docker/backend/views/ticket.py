import os
import uuid
from typing import Dict, List, Tuple

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


def list_ticket_logic(current_user) -> Tuple[str, str, int, List[Dict] or None]:
    try:
        uid = current_user.uid
        priority = current_user.priority

        if priority == 1:
            tickets = get_all_tickets()
        else:
            tickets = get_tickets_by_user(uid)

        if not tickets:
            return "目前沒有發票資料", "success", 200, None

        # 處理結果格式
        results = [{
            "time": t.createdate,
            "type": t.type,
            "title": td.title,
            "money": td.money,
            "state": t.status,
            "number": t.invoice_number
        } for t in tickets for td in t.details]

        return "成功", "success", 200, results

    except Exception as e:
        print(e)
        return "伺服器錯誤", "error", 500, []

def delete_ticket_logic(tid: int, current_user) -> Tuple[str, str, int]:
    try:
        ticket = get_ticket_by_id(tid)
        if not ticket:
            return "找不到該發票", "error", 404

        # status 為 2 表示發票已完成，禁止任何人刪除
        if ticket.status == 2:
            return "無法刪除已完成的發票", "error", 403

        # 一般使用者只能刪除自己的發票
        if current_user.priority == 0 and ticket.uid != current_user.uid:
            return "你無權刪除此發票", "error", 403

        success = delete_ticket_by_id(tid)
        if success:
            return "發票已成功刪除", "success", 200
        return "刪除發票時發生錯誤", "error", 500

    except Exception as e:
        print(e)
        return "伺服器錯誤", "error", 500

def change_ticket_logic(tid: int, payload, current_user) -> Tuple[str, str, int]:
    try:
        if not payload.class_ or not isinstance(payload.detail, list):
            return "請提供 class 和 detail", "error", 400

        ticket = get_ticket_by_id(tid)
        if not ticket:
            return "找不到發票", "error", 404

        if ticket.status == 2:
            return "無法修改已完成的發票", "error", 403

        if current_user.priority == 0 and ticket.uid != current_user.uid:
            return "你無權修改這張發票", "error", 403

        if not update_ticket_class(tid, payload.class_):
            return "更新主分類失敗", "error", 500

        existing_ids = set(get_detail_ids_by_tid(tid))
        new_ids = set()

        for item in payload.detail:
            if item.title is None or item.money is None:
                continue

            if item.id:
                if item.id in existing_ids:
                    success = update_ticket_detail(item.id, tid, item.title, item.money)
                    if not success:
                        return f"更新明細 ID {item.id} 失敗", "error", 500
                    new_ids.add(item.id)
                else:
                    return f"找不到明細 id {item.id}", "error", 400
            else:
                success = create_ticket_detail(tid, item.title, item.money)
                if not success:
                    return "新增明細失敗", "error", 500

        ids_to_delete = existing_ids - new_ids
        if ids_to_delete:
            success = delete_ticket_details_by_ids(ids_to_delete)
            if not success:
                return "刪除舊明細失敗", "error", 500

        return "發票已成功修改", "success", 200

    except Exception as e:
        print(f"[ERROR] 修改發票錯誤：{e}")
        return "修改發票時發生錯誤", "error", 500

def search_ticket_logic(keyword: str, current_user) -> Tuple[str, str, int, List[Dict] or None]:
    try:
        tickets = search_tickets_by_keyword(keyword)

        if not tickets:
            return "查無資料", "error", 404, None

        filtered = []

        for row in tickets:
            if current_user.priority == 0:
                # 一般使用者只能看到自己的票
                if row.uid != current_user.uid:
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
                    "tid": row.tid,
                    "class": row.class_,
                    "uid": row.uid,
                    "status": row.status,
                    "invoice_number": row.invoice_number,
                    "createdate": row.createdate,
                    "title": row.title,
                    "money": row.money
                })

        return "查詢成功", "success", 200, filtered

    except Exception as e:
        print(f"[ERROR] 查詢發票錯誤：{e}")
        return "查詢時發生錯誤", "error", 500, None

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
# 若資料夾不存在會自動建立
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

async def upload_ticket_logic(file: UploadFile, current_user) -> Tuple[str, str, int, List[Dict] or None]:
    if not file or not file.filename:
        return "未選擇檔案", "error", 400, None

    if not allowed_file(file.filename):
        return "不支援的檔案格式", "error", 400, None

    try:
        ext = file.filename.rsplit('.', 1)[1].lower()
        new_filename = f"{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(UPLOAD_FOLDER, new_filename)

        # 儲存檔案
        contents = await file.read()
        with open(save_path, "wb") as f:
            f.write(contents)

        # 建立發票資料
        tid = create_ticket(current_user.uid, new_filename)

        if not tid:
            return "建立發票失敗", "error", 500, None

        return "圖片上傳並建立新發票成功", "success", 200, {
            "filename": new_filename,
            "tid": tid
        }

    except Exception as e:
        print(f"[ERROR] 上傳圖片失敗：{e}")
        return "伺服器錯誤", "error", 500, None

def total_money_logic(current_user) -> Tuple[str, str, int, List[Dict] or None]:
    try:
        total = get_total_money(current_user)
        return "查詢成功", "success", 200, {"total_money": total}
    except Exception as e:
        print(f"[ERROR] 加總 money 失敗：{e}")
        return "加總時發生錯誤", "error", 500, None

def list_class_logic() -> Tuple[str, str, int, List[Dict] or None]:
    try:
        classes = get_distinct_classes()
        return "查詢成功", "success", 200, {"classes": classes}
    except Exception as e:
        print(f"[ERROR] 查詢類別失敗：{e}")
        return "查詢類別時發生錯誤", "error", 500, None

def list_date_logic() -> Tuple[str, str, int, List[Dict] or None]:
    try:
        dates = get_distinct_dates()
        return "查詢成功", "success", 200, {"dates": dates}
    except Exception as e:
        print(f"[ERROR] 查詢日期失敗：{e}")
        return "查詢日期時發生錯誤", "error", 500, None

def unaudited_invoices_logic() -> Tuple[str, str, int, List[Dict] or None]:
    try:
        count = count_status_1()
        return "統計成功", "success", 200, {"status_1_count": count}
    except Exception as e:
        print(f"[ERROR] 統計 status=1 錯誤：{e}")
        return "統計失敗", "error", 500, None

def not_write_off_logic() -> Tuple[str, str, int, List[Dict] or None]:
    try:
        count_0 = count_by_status(0)
        count_1 = count_by_status(1)
        total = count_0 + count_1

        return "統計成功", "success", 200, {"total": total}
    except Exception as e:
        print(f"[ERROR] 統計 Ticket status 錯誤：{e}")
        return "伺服器錯誤", "error", 500, None

def write_off_logic() -> Tuple[str, str, int, List[Dict] or None]:
    try:
        count = count_by_status(2)
        total_money = sum_money_by_status(2)

        return "統計成功", "success", 200, {
            "count": count,
            "total_money": total_money
        }
    except Exception as e:
        print(f"[ERROR] 統計 status=2 與金額加總錯誤：{e}")
        return "伺服器錯誤", "error", 500, None

def audit_ticket_service(tid: int, status: int):
    ticket = get_ticket_by_id(tid)
    if not ticket:
        return "找不到該發票", "error", 404

    if ticket.status == 2:
        return "該發票已完成，無法重新審核", "error", 400

    if update_ticket_status(tid, status):
        return "審核成功", "success", 200

    return "更新資料失敗", "error", 500