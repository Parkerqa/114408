from typing import List, Dict, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from .db_utils import SessionLocal
from .models import Departments, DepartmentAccounting, AccountingItems


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


def get_departments_budget_summary() -> Optional[List[Dict]]:
    db: Session = SessionLocal()
    try:
        rows = (
            db.query(
                Departments.department_id,
                Departments.dept_name,
                func.sum(DepartmentAccounting.budget_limit).label("total_budget")
            )
            .join(DepartmentAccounting, Departments.department_id == DepartmentAccounting.department_id)
            .filter(DepartmentAccounting.is_active == 1)
            .group_by(Departments.department_id, Departments.dept_name)
            .all()
        )

        results = []
        for r in rows:
            results.append({
                "department_id": r.department_id,
                "dept_name": r.dept_name,
                "total_budget": float(r.total_budget) if r.total_budget is not None else 0.0
            })
        return results
    except Exception as e:
        print(f"[ERROR] get_departments_budget_summary failed: {e}")
        return None
    finally:
        db.close()


def get_department_accounts(department_id: int) -> Optional[List[Dict]]:
    db: Session = SessionLocal()
    try:
        rows = (
            db.query(
                AccountingItems.accounting_id,
                AccountingItems.account_name,
                DepartmentAccounting.budget_limit
            )
            .join(DepartmentAccounting, AccountingItems.accounting_id == DepartmentAccounting.accounting_id)
            .filter(
                DepartmentAccounting.department_id == department_id,
                DepartmentAccounting.is_active == 1
            )
            .all()
        )

        results = []
        for r in rows:
            results.append({
                "accounting_id": r.accounting_id,
                "account_name": r.account_name,
                "budget_limit": float(r.budget_limit) if r.budget_limit is not None else 0.0
            })
        return results
    except Exception as e:
        print(f"[ERROR] get_department_accounts failed: {e}")
        return None
    finally:
        db.close()
