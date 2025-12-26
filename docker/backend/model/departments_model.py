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


def get_departments_with_accounts() -> Optional[List[Dict]]:
    db: Session = SessionLocal()
    try:
        rows = (
            db.query(
                Departments.department_id,
                Departments.dept_name,
                AccountingItems.accounting_id,
                AccountingItems.account_name,
                DepartmentAccounting.budget_limit
            )
            .outerjoin(DepartmentAccounting, Departments.department_id == DepartmentAccounting.department_id)
            .outerjoin(AccountingItems, AccountingItems.accounting_id == DepartmentAccounting.accounting_id)
            .filter(Departments.is_active == 1)
            .all()
        )

        dept_map: Dict[int, Dict] = {}
        for r in rows:
            if r.department_id not in dept_map:
                dept_map[r.department_id] = {
                    "department_id": r.department_id,
                    "dept_name": r.dept_name,
                    "accounts": []
                }
            if r.accounting_id:
                dept_map[r.department_id]["accounts"].append({
                    "accounting_id": r.accounting_id,
                    "account_name": r.account_name,
                    "budget_limit": float(r.budget_limit) if r.budget_limit else 0.0
                })

        return list(dept_map.values())

    except Exception as e:
        print(f"[ERROR] get_departments_with_accounts failed: {e}")
        return None
    finally:
        db.close()


def sync_department_accountings(department_id: int, accounting_items: list, updated_by: int) -> bool:
    db: Session = SessionLocal()
    try:
        # 1. DB 目前有哪些 accounting_id
        existing = db.query(DepartmentAccounting).filter(
            DepartmentAccounting.department_id == department_id
        ).all()
        existing_map = {d.accounting_id: d for d in existing}

        incoming_ids = {item.accounting_id for item in accounting_items}

        # 2. 更新 & 新增
        for item in accounting_items:
            if item.accounting_id in existing_map:
                # 更新
                db.query(DepartmentAccounting).filter(
                    DepartmentAccounting.department_id == department_id,
                    DepartmentAccounting.accounting_id == item.accounting_id
                ).update({
                    DepartmentAccounting.budget_limit: item.budget_limit,
                    DepartmentAccounting.updated_by: updated_by
                })
            else:
                # 新增
                new_acc = DepartmentAccounting(
                    department_id=department_id,
                    accounting_id=item.accounting_id,
                    budget_limit=item.budget_limit,
                    created_by=updated_by,
                    updated_by=updated_by
                )
                db.add(new_acc)

        # 3. 刪除 DB 裡有但前端沒傳的
        to_delete_ids = set(existing_map.keys()) - incoming_ids
        if to_delete_ids:
            db.query(DepartmentAccounting).filter(
                DepartmentAccounting.department_id == department_id,
                DepartmentAccounting.accounting_id.in_(to_delete_ids)
            ).delete(synchronize_session=False)

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()