from sqlalchemy.orm import Session

from .db_utils import SessionLocal
from .models import Ticket, TicketDetail

def save_error(ticket_id):
    db: SessionLocal = SessionLocal()
    try:
        db.query(Ticket).filter(Ticket.ticket_id == ticket_id).update({
            Ticket.type: 0,
            Ticket.status: 0
        })
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    finally:
        db.close()

# save ocr output
def save_ocr_result(ticket_id, invoice_type, catch_result):
    db: Session = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).one_or_none()
        if not ticket:
            return False

        ticket.type = invoice_type
        ticket.invoice_number = catch_result["invoice_number"]
        ticket.date = catch_result["date"]
        ticket.total_money = catch_result["total_money"]
        ticket.status = 2
        ticket.modify_id = 0

        titles = catch_result.get("title", [])
        moneys = catch_result.get("money", [])

        if titles and moneys and len(titles) == len(moneys):
            details = [
                TicketDetail(
                    ticket_id=ticket_id,
                    title=title,
                    money=money
                )
                for title, money in zip(titles, moneys)
            ]
            db.add_all(details)
        db.commit()
        return True
    except Exception as e:
        print(f"[ERROR] 儲存 OCR 結果失敗：{e}")
        db.rollback()
        return False
    finally:
        db.close()

# save qrcode decoder output
def save_qrcode_result(ticket_id, invoice_type, catch_result, items):
    db: Session = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).one_or_none()
        ticket.type = invoice_type
        ticket.invoice_number = catch_result["invoice_number"]
        ticket.date = catch_result["date"]
        ticket.total_money = catch_result["total_money"]
        ticket.status = 2
        ticket.modify_id = 0

        for item in items:
            detail = TicketDetail(
                ticket_id=ticket_id,
                title=item["title"],
                money=item["money"]
            )
            db.add(detail)
        db.commit()
        return True
    except Exception as e:
        print(f"[ERROR] 儲存 QRcode Decorder 結果失敗：{e}")
        db.rollback()
        return False
    finally:
        db.close()