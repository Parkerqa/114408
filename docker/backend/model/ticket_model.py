from typing import List, Optional

from sqlalchemy import String, cast, func, or_
from sqlalchemy.orm import Session, aliased

from .db_utils import SessionLocal
from .models import Ticket, TicketDetail


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
        result = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).update({Ticket.class_: new_class})
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
            TicketDetail.money: money
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


def search_tickets_by_keyword(keyword: str):
    db: Session = SessionLocal()
    try:
        # 為了 JOIN 與欄位存取一致，手動建立 alias
        t = aliased(Ticket)
        td = aliased(TicketDetail)

        return db.query(t, t.user_id, td.title, td.money) \
            .outerjoin(td, t.ticket_id == td.ticket_id) \
            .filter(
            or_(
                t.createdate.like(f"%{keyword}%"),
                t.class_.like(f"%{keyword}%"),
                t.invoice_number.like(f"%{keyword}%"),
                td.title.like(f"%{keyword}%"),
                cast(td.money, String).like(f"%{keyword}%")
            )
        ).all()
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def create_ticket(user_id: int, img_filename: str) -> int | None:
    db: Session = SessionLocal()
    try:
        ticket = Ticket(user_id=user_id, img=img_filename, status=1, create_id=user_id, modify_id=user_id,
                        available=True)
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


def get_distinct_classes() -> list[str] or None:
    db: Session = SessionLocal()
    try:
        results = db.query(Ticket.class_).distinct().all()
        return [r[0] for r in results if r[0] is not None]
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()


def get_distinct_dates() -> list[str] or None:
    db: Session = SessionLocal()
    try:
        results = db.query(
            func.date_format(Ticket.createdate, "%Y/%m/%d")
        ).distinct().all()
        return [r[0] for r in results if r[0] is not None]
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


def update_ticket_status(ticket_id: int, status: int) -> bool:
    db: Session = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
        if ticket:
            ticket.status = status
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"[ERROR] 更新發票狀態失敗：{e}")
        return False
    finally:
        db.close()
