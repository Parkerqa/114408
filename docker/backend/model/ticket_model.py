from sqlalchemy import String, cast, func, or_
from sqlalchemy.orm import Session, aliased

from .db_utils import SessionLocal
from .models import Ticket, TicketDetail


def get_all_tickets():
    db: Session = SessionLocal()
    try:
        return db.query(Ticket).all()
    except Exception as e:
        print(e)
        return None

def get_tickets_by_user(uid: int):
    db: Session = SessionLocal()
    try:
        return db.query(Ticket).filter(Ticket.uid == uid).all()
    except Exception as e:
        print(e)
        return None

def get_ticket_by_id(tid: int):
    db: Session = SessionLocal()
    try:
        return db.query(Ticket).filter(Ticket.tid == tid).first()
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()

def delete_ticket_by_id(tid: int) -> bool:
    db: Session = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.tid == tid).first()
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

def update_ticket_class(tid: int, new_class: str) -> bool:
    db: Session = SessionLocal()
    try:
        result = db.query(Ticket).filter(Ticket.tid == tid).update({Ticket.class_: new_class})
        db.commit()
        return result > 0
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()

def get_detail_ids_by_tid(tid: int):
    db: Session = SessionLocal()
    try:
        return [d.td_id for d in db.query(TicketDetail.td_id).filter(TicketDetail.tid == tid).all()]
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()

def update_ticket_detail(td_id: int, tid: int, title: str, money: str) -> bool:
    db: Session = SessionLocal()
    try:
        result = db.query(TicketDetail).filter(
            TicketDetail.td_id == td_id,
            TicketDetail.tid == tid
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

def create_ticket_detail(tid: int, title: str, money: str) -> bool:
    db: Session = SessionLocal()
    try:
        new_detail = TicketDetail(tid=tid, title=title, money=money)
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

        return db.query(t, t.uid, td.title, td.money)\
            .outerjoin(td, t.tid == td.tid)\
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

def create_ticket(uid: int, img_filename: str) -> int | None:
    db: Session = SessionLocal()
    try:
        ticket = Ticket(uid=uid, img=img_filename, status=0)
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket.tid
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
            query = query.join(Ticket, Ticket.tid == TicketDetail.tid).filter(Ticket.uid == current_user.uid)
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
        result = db.query(func.sum(TicketDetail.money))\
            .join(Ticket, TicketDetail.tid == Ticket.tid)\
            .filter(Ticket.status == status).scalar()
        return result or 0
    except Exception as e:
        print(e)
        return None
    finally:
        db.close()

def update_ticket_status(tid: int, status: int) -> bool:
    db: Session = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.tid == tid).first()
        if ticket:
            ticket.status = status
            db.commit()
            db.refresh(ticket)
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"[ERROR] 更新發票狀態失敗：{e}")
        return False
    finally:
        db.close()