from sqlalchemy.orm import Session
from .db_utils import SessionLocal
from .models import Departments


def department_exists(name: str) -> bool:
    db: Session = SessionLocal()
    try:
        return db.query(Departments).filter(Departments.name == name).first() is not None
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()


def create_department(name: str, money_limit: str) -> bool:
    db: Session = SessionLocal()
    try:
        new_item = Departments(name=name, money_limit=money_limit)
        db.add(new_item)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()


def get_department_by_id(dept_id: int):
    db: Session = SessionLocal()
    try:
        return db.query(Departments).filter(Departments.dept_id == dept_id).first()
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def update_department_by_id(dept_id: int, new_name: str, new_money_limit: str) -> bool:
    db: Session = SessionLocal()
    try:
        result = db.query(Departments).filter(Departments.dept_id == dept_id).update({
            Departments.name: new_name,
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


def delete_department_by_id(dept_id: int) -> bool:
    db: Session = SessionLocal()
    try:
        obj = db.query(Departments).filter(Departments.dept_id == dept_id).first()
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