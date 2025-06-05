from sqlalchemy.orm import Session

from .db_utils import SessionLocal
from .models import Accounting


def get_account_classes_by_class(class_: str) -> list[str] or None:
    db: Session = SessionLocal()
    try:
        results = db.query(Accounting.account_class).filter(Accounting.class_ == class_).all()
        return [r[0] for r in results if r[0] is not None]
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()
