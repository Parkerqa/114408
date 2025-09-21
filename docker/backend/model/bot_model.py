from sqlalchemy.orm import Session
from views.checker import check_status

from .db_utils import SessionLocal
from .models import Ticket


# get awaiting ticket img (test)
def get_awaiting_ticket_by_uid(user_id: int, ticket_id: int):
    db: Session = SessionLocal()
    try:
        result = db.query(Ticket).filter(Ticket.create_by == user_id, Ticket.ticket_id == ticket_id).first()
        if result and result.img:
            return f"https://devapi.micky.codes/static/invoice/{result.img}"
        else:
            return None
    except Exception:
        return None
    finally:
        db.close()


# get awaiting ticket (test)
def get_awaiting_ticket_info_by_uid(user_id: int, ticket_id: int):
    db: Session = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(
            Ticket.ticket_id == ticket_id,
            Ticket.create_by == user_id,
            Ticket.status == 2
        ).first()

        if not ticket:
            return "查無符合的待審核發票"

        header = (
            f"發票編號：{ticket.invoice_number}\n"
            f"申請日期：{ticket.created_at.strftime('%Y-%m-%d')}\n"
            f"狀態：{check_status(ticket.status)}\n"
        )

        if ticket.ticket_details:
            detail_lines = [
                f"{idx + 1}. 項目：{td.title}，金額：{int(td.money)} 元"
                for idx, td in enumerate(ticket.ticket_details)
            ]
            detail_text = "\n\n".join(detail_lines)
        else:
            detail_text = "尚無明細資料"

        return header + "\n明細：\n\n" + detail_text

    except Exception as e:
        print(e)
        return "查詢失敗"
    finally:
        db.close()


# get awaiting ticket list (test)
def get_awaiting_list_by_uid(user_id: int):
    db: Session = SessionLocal()
    try:
        results = db.query(Ticket).filter(
            Ticket.create_by == user_id, Ticket.status == 2
        ).all()

        if results:
            header = f"您有 {len(results)} 筆待處理發票：\n\n"
            messages = [
                f"{idx + 1}. 申請日期：{t.created_at.strftime('%Y-%m-%d')}\n    發票號碼：{t.invoice_number}\n    狀態：{check_status(t.status)}"
                for idx, t in enumerate(results)
            ]
            return header + "\n\n".join(messages)
        else:
            return "您尚未上傳任何待處理發票"
    except Exception:
        return "查詢失敗"
    finally:
        db.close()
