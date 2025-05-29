from sqlalchemy.orm import Session

from .db_utils import SessionLocal
from .models import TicketDetail


# save output
def save_result(catch_result):
    db: Session = SessionLocal()
    try:
        result = TicketDetail(
            tid=catch_result["TID"],
            title=catch_result["title"],
            money=catch_result["money"]
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return True
    except Exception as e:
        print(f"[ERROR] 儲存 OCR 結果失敗：{e}")
        db.rollback()
        return False
    finally:
        db.close()