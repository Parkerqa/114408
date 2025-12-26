from sqlalchemy import func, cast, Numeric, literal, case, and_
from sqlalchemy.types import Numeric
from sqlalchemy.orm import Session

from .db_utils import SessionLocal
from .models import AccountingItems, Departments, DepartmentAccounting


def get_account_classes_by_class(class_: str) -> list[str] or None:
    db: Session = SessionLocal()
    try:
        results = db.query(AccountingItems.account_class).filter(AccountingItems.class_ == class_).all()
        return [r[0] for r in results if r[0] is not None]
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def get_all_classes_info() -> list[dict] | None:
    db: Session = SessionLocal()
    try:
        query = (
            db.query(
                AccountingItems.account_name.label("account_name"),
                # 只把「啟用中的關聯 + 啟用中的部門」的預算納入合計
                func.coalesce(
                    func.sum(
                        case(
                            (
                                and_(
                                    Departments.is_active == 1,
                                    DepartmentAccounting.is_active == 1
                                ),
                                DepartmentAccounting.budget_limit
                            ),
                            else_=0
                        )
                    ),
                    0
                ).label("total_budget"),
                cast(literal(0), Numeric(12, 2)).label("total_amount"),
            )
            # 多對多關聯：會計項目 ←(外連結)→ 部門×科目 ←(外連結)→ 部門
            .outerjoin(
                DepartmentAccounting,
                DepartmentAccounting.accounting_id == AccountingItems.accounting_id
            )
            .outerjoin(
                Departments,
                Departments.department_id == DepartmentAccounting.department_id
            )
            # 只取啟用中的會計項目
            .filter(AccountingItems.is_active == 1)
            .group_by(AccountingItems.account_name)
            .order_by(AccountingItems.account_name.asc())
        )

        rows = query.all()
        return [
            {
                "account_name": r.account_name,
                "total_budget": float(r.total_budget or 0),
                "total_amount": float(r.total_amount or 0),
            }
            for r in rows
        ]
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()
