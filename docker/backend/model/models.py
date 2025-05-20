import datetime
from typing import List, Optional

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Accounting(Base):
    __tablename__ = 'accounting'

    acid: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_: Mapped[Optional[str]] = mapped_column('class', String(45))
    account_class: Mapped[Optional[str]] = mapped_column(String(45))


class ClassInfo(Base):
    __tablename__ = 'class_info'

    cid: Mapped[int] = mapped_column(Integer, primary_key=True)
    money_limit: Mapped[Optional[str]] = mapped_column(String(45))
    class_: Mapped[Optional[str]] = mapped_column('class', String(45))


class OtherSetting(Base):
    __tablename__ = 'other_setting'

    uid: Mapped[int] = mapped_column(Integer, primary_key=True)
    theme: Mapped[Optional[int]] = mapped_column(Integer)
    red_but: Mapped[Optional[int]] = mapped_column(Integer)
    red_top: Mapped[Optional[int]] = mapped_column(Integer)
    green_but: Mapped[Optional[int]] = mapped_column(Integer)
    green_top: Mapped[Optional[int]] = mapped_column(Integer)
    yellow_but: Mapped[Optional[int]] = mapped_column(Integer)
    yellow_top: Mapped[Optional[int]] = mapped_column(Integer)


class Ticket(Base):
    __tablename__ = 'ticket'

    tid: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_: Mapped[Optional[str]] = mapped_column('class', String(45))
    uid: Mapped[Optional[int]] = mapped_column(Integer)
    check_man: Mapped[Optional[str]] = mapped_column(String(45))
    check_date: Mapped[Optional[str]] = mapped_column(String(45))
    img: Mapped[Optional[str]] = mapped_column(String(45))
    status: Mapped[Optional[int]] = mapped_column(Integer)
    createid: Mapped[Optional[str]] = mapped_column(String(45))
    createdate: Mapped[Optional[datetime.date]] = mapped_column(Date)
    modifyid: Mapped[Optional[str]] = mapped_column(String(45))
    modifydate: Mapped[Optional[str]] = mapped_column(String(45))
    available: Mapped[Optional[str]] = mapped_column(String(45))
    writeoff_date: Mapped[Optional[str]] = mapped_column(String(45))
    type: Mapped[Optional[str]] = mapped_column(String(45))
    invoice_number: Mapped[Optional[str]] = mapped_column(String(45))

    # Ticket → TicketDetail 一對多
    details: Mapped[List["TicketDetail"]] = relationship(
        back_populates="ticket",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class TicketDetail(Base):
    __tablename__ = 'ticket_detail'

    td_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # 關聯欄位從 String 改為 Integer + ondelete
    tid: Mapped[int] = mapped_column(ForeignKey('ticket.tid', ondelete='CASCADE'))

    title: Mapped[Optional[str]] = mapped_column(String(45))
    money: Mapped[Optional[str]] = mapped_column(String(45))

    # 回到主表 Ticket
    ticket: Mapped["Ticket"] = relationship(back_populates="details")


class User(Base):
    __tablename__ = 'User'

    uid: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(45))
    password: Mapped[str] = mapped_column(String(100))
    username: Mapped[Optional[str]] = mapped_column(String(45))
    priority: Mapped[Optional[int]] = mapped_column(Integer)
    img: Mapped[Optional[str]] = mapped_column(String(45))