from .models import Ailog
from .db_utils import SessionLocal

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