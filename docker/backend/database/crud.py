from sqlalchemy.orm import Session

from .db_utils import SessionLocal
from .models import Ailog, TicketDetail

# 儲存 OCR 結果到 ticket_detail 表
def post_ticket_detail(catch_result):
    db: Session = SessionLocal()
    try:
        result = TicketDetail(
            TID=catch_result.get("TID"),
            time=catch_result.get("time"),
            title=catch_result.get("title"),
            money=catch_result.get("money")
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return {
            "message": "success",
            "filename": catch_result.get("title")
        }
    except Exception as e:
        db.rollback()
        print(f"[ERROR] post_ticket_detail failed: {e}")
        return {"message": "fail", "error": str(e)}
    finally:
        db.close()

# 取得 AILog 資料表中第一筆紀錄
def get_ailog():
    db: Session = SessionLocal()
    try:
        result = db.query(Ailog).first()
        if result:
            return f"aid：{result.AID}, log：{result.log}"
        else:
            return "資料庫中沒有資料"
    except Exception as e:
        print(f"[ERROR] get_ailog failed: {e}")
        return "資料庫查詢失敗"
    finally:
        db.close()