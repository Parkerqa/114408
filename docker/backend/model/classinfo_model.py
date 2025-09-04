from sqlalchemy.orm import Session

from .db_utils import SessionLocal
from .models import Departments


def class_exists(class_name: str) -> bool:
    db: Session = SessionLocal()
    try:
        return db.query(Departments).filter(Departments.class_ == class_name).first() is not None
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()


def create_class(class_: str, money_limit: str) -> bool:
    db: Session = SessionLocal()
    try:
        new_item = Departments(class_=class_, money_limit=money_limit)
        db.add(new_item)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()


def get_class_by_id(cid: int):
    db: Session = SessionLocal()
    try:
        return db.query(Departments).filter(Departments.cid == cid).first()
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def update_class_by_id(cid: int, new_class: str, new_money_limit: str) -> bool:
    db: Session = SessionLocal()
    try:
        result = db.query(Departments).filter(Departments.cid == cid).update({
            Departments.class_: new_class,
            Departments.money_limit: new_money_limit
        })
        db.commit()
        return result > 0
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()


def delete_class_by_id(cid: int) -> bool:
    db: Session = SessionLocal()
    try:
        obj = db.query(Departments).filter(Departments.cid == cid).first()
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()
