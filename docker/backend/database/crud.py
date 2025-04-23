from sqlalchemy.orm import Session

from .db_utils import SessionLocal
from .models import Ailog, TicketDetail


def get_ailog():
    db = SessionLocal()
    try:
        result = db.query(Ailog).first()
        if result:
            return f"aid：{result.AID}, log：{result.log}"
        else:
            return "資料庫中沒有資料"
    finally:
        db.close()

def post_ticket_detail(db: Session, catch_result):
    db = SessionLocal()
    try:
        result = TicketDetail(TID=catch_result["TID"], time=catch_result["time"], title=catch_result["title"],money=catch_result["money"])
        db.add(result)
        db.commit()
        db.refresh(result)
        return {"message": "success", "filename": catch_result["title"]}
    finally:
        db.close()


