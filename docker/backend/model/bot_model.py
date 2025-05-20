from sqlalchemy.orm import Session

from .db_utils import SessionLocal
from .models import Ticket


# get ticket (test)
def get_ticket_by_uid(uid: int):
    db: Session = SessionLocal()
    try:
        result = db.query(Ticket).filter(Ticket.uid == uid).first()
        if result:
            return f"您最新的票據：{result.invoice_number}，狀態：{result.status}"
        else:
            return "您尚未上傳任何發票"
    except Exception:
        return "查詢失敗"
    finally:
        db.close()