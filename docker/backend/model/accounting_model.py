from sqlalchemy import func, literal, cast
from sqlalchemy.types import Numeric
from sqlalchemy.orm import Session

from .db_utils import SessionLocal
from .models import Accounting, Department


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


def get_all_classes_info() -> list[dict] | None:
    """
    回傳每個會計科目的：account_class、total_budget、total_amount(暫為 0)
    total_budget: sum(class_info.money_limit)
    total_amount: 先以 0 回傳（尚無支出明細）
    """
    db: Session = SessionLocal()
    try:
        query = (
            db.query(
                Accounting.account_class.label("account_class"),
                func.coalesce(func.sum(Department.money_limit), 0).label("total_budget"),
                cast(literal(0), Numeric(10, 2)).label("total_amount"),  # <<< 這行修正重點
            )
            .join(
                Department,
                Accounting.class_info_id == Department.class_info_id,
                isouter=True
            )
            # 若 avaible 可能為 NULL，建議改成 func.coalesce(Accounting.avaible, 1) == 1
            .filter(Accounting.avaible == 1)
            .group_by(Accounting.account_class)
            .order_by(Accounting.account_class.asc())
        )

        rows = query.all()
        return [
            {
                "account_class": r.account_class,
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
