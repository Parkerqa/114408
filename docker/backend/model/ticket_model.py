import os

from typing import List, Dict, Optional, Any, Set
from sqlalchemy import String, desc, cast, func, or_, and_, Date
from sqlalchemy.orm import Session, aliased, joinedload
from datetime import datetime, timedelta, date as date_cls
from decimal import Decimal

from .db_utils import SessionLocal
from .models import User, Ticket, TicketDetail, AccountingItems, DepartmentAccounting
from views.checker import check_type, check_status
from constants.ticket_status import TicketStatus, FINAL_STATES


def get_all_tickets(status: Optional[List[int]]):
    db: Session = SessionLocal()
    try:
        if status:
            return db.query(Ticket).filter(Ticket.status.in_(status)).all()
        return db.query(Ticket).all()
    except Exception as e:
        print(e)
        return None


def get_tickets_by_user(user_id: int, status: Optional[List[int]]):
    db: Session = SessionLocal()
    try:
        if status:
            return db.query(Ticket).filter(Ticket.user_id == user_id, Ticket.status.in_(status)).all()
        return db.query(Ticket).filter(Ticket.user_id == user_id).all()
    except Exception as e:
        print(e)
        return None


def get_specify_ticket(user_id: int, ticket_id: int):
    db: Session = SessionLocal()
    try:
        return db.query(Ticket).filter(Ticket.user_id == user_id, Ticket.ticket_id == ticket_id).one()
    except Exception as e:
        print(e)
        return None


def get_ticket_by_id(ticket_id: int):
    db: Session = SessionLocal()
    try:
        return db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def update_ticket_info(ticket_id: int, type_: Optional[int], invoice_number: Optional[str], total_money: str) -> bool:
    db: Session = SessionLocal()
    try:
        updates = {}
        if type_ is not None:
            updates[Ticket.type] = type_
        if invoice_number is not None:
            updates[Ticket.invoice_number] = invoice_number
        if total_money is not None:
            updates[Ticket.total_money] = Decimal(total_money)

        if not updates:
            return True

        result = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).update(updates)
        db.commit()
        return result > 0
    except Exception as e:
        db.rollback()
        print(f"[ERROR] update_ticket_info failed: {e}")
        return False
    finally:
        db.close()


def get_tickets_by_ids(ticket_ids: List[int]) -> Optional[List[Ticket]]:
    db: Session = SessionLocal()
    try:
        return db.query(Ticket).filter(Ticket.ticket_id.in_(ticket_ids)).all()
    except Exception as e:
        print(e)
        return None


def delete_ticket_by_id(ticket_id: int) -> bool:
    db: Session = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
        if not ticket:
            return False
        db.delete(ticket)  # 因為關聯已設 cascade delete，細節也會一起刪
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()


def update_ticket_class(ticket_id: int, new_class: str) -> bool:
    db: Session = SessionLocal()
    try:
        result = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).update({Ticket.accounting_id: new_class})
        db.commit()
        return result > 0
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()


def get_detail_ids_by_tid(ticket_id: int):
    db: Session = SessionLocal()
    try:
        return [d.td_id for d in db.query(TicketDetail.td_id).filter(TicketDetail.ticket_id == ticket_id).all()]
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def update_ticket_detail(td_id: int, ticket_id: int, title: str, money: str) -> bool:
    db: Session = SessionLocal()
    try:
        result = db.query(TicketDetail).filter(
            TicketDetail.td_id == td_id,
            TicketDetail.ticket_id == ticket_id
        ).update({
            TicketDetail.title: title,
            TicketDetail.money: Decimal(money)
        })
        db.commit()
        return result > 0
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()


def create_ticket_detail(ticket_id: int, title: str, money: str) -> bool:
    db: Session = SessionLocal()
    try:
        new_detail = TicketDetail(ticket_id=ticket_id, title=title, money=money)
        db.add(new_detail)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()


def delete_ticket_details_by_ids(td_ids: set) -> bool:
    db: Session = SessionLocal()
    try:
        result = db.query(TicketDetail).filter(TicketDetail.td_id.in_(td_ids)).delete(synchronize_session=False)
        db.commit()
        return result > 0
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()


def search_tickets_combined(
    status: List[int],
    keyword: Optional[str] = None,
    date: Optional[date_cls] = None,
    limit: int = 50,
) -> Optional[List[Ticket]]:
    db: Session = SessionLocal()
    try:
        q = (
            db.query(Ticket)
            .options(joinedload(Ticket.ticket_detail))
        )

        filters = [Ticket.status.in_(status)]

        # 關鍵字模糊搜尋
        if keyword:
            like = f"%{keyword}%"
            filters.append(
                or_(
                    cast(Ticket.created_at, String).ilike(like),
                    Ticket.invoice_number.ilike(like),
                    TicketDetail.title.ilike(like),
                    cast(TicketDetail.money, String).ilike(like),
                )
            )

        # 日期過濾
        if date:
            filters.append(cast(Ticket.created_at, Date) == date)

        q = q.outerjoin(TicketDetail, TicketDetail.ticket_id == Ticket.ticket_id) \
             .filter(and_(*filters)) \
             .order_by(desc(Ticket.created_at)) \
             .limit(limit)

        return q.all()

    except Exception as e:
        print(f"[ERROR] search_tickets_combined failed: {e}")
        return None
    finally:
        db.close()


def create_ticket(user_id: int, img_filename: str) -> int | None:
    db: Session = SessionLocal()
    try:
        ticket = Ticket(user_id=user_id, img=img_filename, status=1, created_by=user_id, updated_by=user_id)
        db.add(ticket)
        db.commit()
        return ticket.ticket_id
    except Exception as e:
        db.rollback()
        print(e)
        return None
    finally:
        db.close()


def get_total_money(current_user) -> int | None:
    db: Session = SessionLocal()
    try:
        query = db.query(func.sum(TicketDetail.money))
        if current_user.priority == 0:
            # 一般用戶只能查自己的發票
            query = query.join(Ticket, Ticket.ticket_id == TicketDetail.ticket_id).filter(
                Ticket.user_id == current_user.user_id)
        total = query.scalar()
        return total if total is not None else 0
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def count_status_1() -> int or None:
    db: Session = SessionLocal()
    try:
        result = db.query(func.count()).select_from(Ticket).filter(Ticket.status == 1).scalar()
        return result or 0
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def count_by_status(status: int) -> int or None:
    db: Session = SessionLocal()
    try:
        result = db.query(func.count()).filter(Ticket.status == status).scalar()
        return result or 0
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def sum_money_by_status(status: int) -> int or None:
    db: Session = SessionLocal()
    try:
        result = db.query(func.sum(TicketDetail.money)) \
            .join(Ticket, TicketDetail.ticket_id == Ticket.ticket_id) \
            .filter(Ticket.status == status).scalar()
        return result or 0
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def bulk_update_ticket_status(payload, checker_user_id: int) -> Dict[str, Any]:
    db: Session = SessionLocal()
    try:
        id_set: Set[int] = {int(item.ticket_id) for item in payload.items}
        if not id_set:
            return {"updated_count": 0, "updated_ids": [], "skipped": [], "not_found": [], "invalid_status": []}

        tickets: List[Ticket] = db.query(Ticket).filter(Ticket.ticket_id.in_(id_set)).all()
        exists_map = {t.ticket_id: t for t in tickets}

        not_found: List[int] = [tid for tid in id_set if tid not in exists_map]
        skipped: List[Dict[str, Any]] = []
        updated_ids: List[int] = []
        invalid_status: List[Dict[str, Any]] = []

        now = datetime.utcnow()

        for item in payload.items:
            tid = int(item.ticket_id)
            new_status = int(item.status)

            # 狀態檢查（避免寫入不合法值）
            if new_status not in [s.value for s in TicketStatus]:
                invalid_status.append({"ticket_id": tid, "reason": f"不合法狀態: {new_status}"})
                continue

            t = exists_map.get(tid)
            if t is None:
                continue

            # 已完成的票不可再審
            if t.status in [s.value for s in FINAL_STATES]:
                skipped.append({"ticket_id": tid, "reason": "該發票已完成審核，無法重新修改"})
                continue

            # 更新狀態
            t.status = new_status

            if new_status in (TicketStatus.APPROVED, TicketStatus.REJECTED):
                if hasattr(t, "check_man"):
                    t.check_man = checker_user_id
                if hasattr(t, "check_date"):
                    t.check_date = now

            updated_ids.append(tid)

        db.commit()

        return {
            "updated_count": len(updated_ids),
            "updated_ids": updated_ids,
            "skipped": skipped,
            "not_found": not_found,
            "invalid_status": invalid_status,
        }

    except Exception as e:
        db.rollback()
        print(f"[ERROR] bulk_update_ticket_status: {e}")
        raise
    finally:
        db.close()


def get_latest_approved(limit: int = 4) -> Optional[List[Dict]]:
    db: Session = SessionLocal()
    try:
        q = (
            db.query(
                Ticket.ticket_id,
                Ticket.type,
                Ticket.invoice_number,
                Ticket.accounting_id,
                Ticket.user_id,
                Ticket.check_man,
                Ticket.check_date,
                Ticket.img,
                Ticket.date,
                Ticket.total_money,
                Ticket.created_at,
                TicketDetail.title.label("title"),
            )
            .join(TicketDetail, TicketDetail.ticket_id == Ticket.ticket_id, isouter=True)
            .filter(Ticket.status == 3)
            .order_by(desc(Ticket.check_date))
            .limit(limit)
        )

        rows = q.all()
        results = []
        for r in rows:
            results.append({
                "upload_date": r.created_at.strftime("%Y-%m-%d") if r.created_at else None,
                "type": check_type(r.type),
                "title": r.title,
                "total_money": float(r.total_money) if r.total_money is not None else None,
            })
        return results

    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def get_pending_reimbursements(limit: int = 20):
    db: Session = SessionLocal()
    try:
        q = (
            db.query(
                Ticket.ticket_id,
                Ticket.created_at.label("upload_date"),
                Ticket.type,
                TicketDetail.title.label("title"),
                Ticket.total_money,
                User.username.label("creator_name"),
                Ticket.check_man,
                Ticket.img,
            )
            .join(TicketDetail, TicketDetail.ticket_id == Ticket.ticket_id, isouter=True)
            .join(User, User.user_id == Ticket.created_by, isouter=True)
            .filter(Ticket.status == 2)
            .order_by(desc(Ticket.created_at))
            .limit(limit)
        )

        rows = q.all()

        grouped = {}
        for r in rows:
            if r.ticket_id not in grouped:
                grouped[r.ticket_id] = {
                    "ticket_id": r.ticket_id,
                    "upload_date": r.upload_date.strftime("%Y-%m-%d") if r.upload_date else None,
                    "type": check_type(r.type),
                    "total_money": float(r.total_money) if r.total_money is not None else None,
                    "creator_name": r.creator_name,
                    "check_man": r.check_man,
                    "img_url": f'{os.getenv("BASE_USER_IMAGE_URL")}{r.img}' if r.img else None,
                    "titles": []
                }
            if r.title:  # 有 title 才加
                grouped[r.ticket_id]["titles"].append(r.title)

        # 最後把 titles list 轉成字串
        results = []
        for t in grouped.values():
            t["title"] = ", ".join(t["titles"]) if t["titles"] else "無品項"
            del t["titles"]
            results.append(t)

        return results

    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def get_approved_records(limit: int = 20):
    db: Session = SessionLocal()
    try:
        q = (
            db.query(
                Ticket.ticket_id,
                Ticket.created_at.label("upload_date"),
                Ticket.type,
                Ticket.total_money,
                User.username.label("creator_name"),
                Ticket.check_man,
                Ticket.status,
                Ticket.img,
                TicketDetail.td_id,
                TicketDetail.title,
                TicketDetail.money,
            )
            .join(TicketDetail, TicketDetail.ticket_id == Ticket.ticket_id, isouter=True)
            .join(User, User.user_id == Ticket.created_by, isouter=True)
            .filter(Ticket.status.in_([3, 4]))
            .order_by(desc(Ticket.check_date))
            .limit(limit)
        )

        rows = q.all()

        ticket_map = {}
        for r in rows:
            if r.ticket_id not in ticket_map:
                ticket_map[r.ticket_id] = {
                    "ticket_id": r.ticket_id,
                    "upload_date": r.upload_date.strftime("%Y-%m-%d") if r.upload_date else None,
                    "type": check_type(r.type),
                    "total_money": float(r.total_money) if r.total_money is not None else None,
                    "creator_name": r.creator_name,
                    "check_man": r.check_man,
                    "status": check_status(r.status),
                    "img_url": f'{os.getenv("BASE_USER_IMAGE_URL")}{r.img}' if r.img else None,
                    "Details": [],
                }

            if r.title:
                ticket_map[r.ticket_id]["Details"].append({
                    "id": r.td_id,
                    "title": r.title,
                    "money": int(r.money) if r.money is not None else 0,
                })

        return list(ticket_map.values())

    except Exception as e:
        print(f"[ERROR] get_approved_records failed: {e}")
        return None
    finally:
        db.close()


def get_tickets_in_range(start_date: date_cls, end_date: date_cls):
    db: Session = SessionLocal()
    try:
        return (
            db.query(Ticket)
            .filter(Ticket.created_at >= start_date, Ticket.created_at <= end_date)
            .options(
                joinedload(Ticket.ticket_detail),
                joinedload(Ticket.user)
            )
            .all()
        )
    finally:
        db.close()


def get_top_accounting_in_range(start_date: date_cls, end_date: date_cls, limit: int = 3):
    db: Session = SessionLocal()
    try:
        rows = (
            db.query(
                AccountingItems.account_class,
                func.sum(Ticket.total_money).label("total_amount"),
                func.sum(DepartmentAccounting.budget_limit).label("total_budget"),
            )
            .join(Ticket, Ticket.accounting_id == AccountingItems.accounting_id)
            .join(DepartmentAccounting, DepartmentAccounting.accounting_id == AccountingItems.accounting_id)
            .filter(Ticket.created_at >= start_date, Ticket.created_at <= end_date)
            .group_by(AccountingItems.account_class)
            .order_by(desc(func.sum(Ticket.total_money)))
            .limit(limit)
            .all()
        )
        return [
            {
                "account_class": r.account_class,
                "total_budget": float(r.total_budget) if r.total_budget else 0.0,
                "total_amount": float(r.total_amount) if r.total_amount else 0.0
            }
            for r in rows
        ]
    finally:
        db.close()


def get_daily_amounts_in_range(start_date: date_cls, end_date: date_cls):
    db: Session = SessionLocal()
    try:
        rows = (
            db.query(
                cast(Ticket.created_at, Date).label("day"),
                func.sum(Ticket.total_money).label("money")
            )
            .filter(Ticket.created_at >= start_date, Ticket.created_at <= end_date)
            .group_by(cast(Ticket.created_at, Date))
            .order_by(cast(Ticket.created_at, Date))
            .all()
        )

        return [
            {"id": idx + 1, "money": float(r.money) if r.money else 0.0}
            for idx, r in enumerate(rows)
        ]
    finally:
        db.close()