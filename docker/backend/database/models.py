from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Accounting(Base):
    __tablename__ = 'accounting'

    ACID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Class: Mapped[str] = mapped_column(String(45))
    account_class: Mapped[str] = mapped_column(String(45))
    creatid: Mapped[str] = mapped_column(String(45))
    createdate: Mapped[str] = mapped_column(String(45))
    modifyid: Mapped[str] = mapped_column(String(45))
    modifydate: Mapped[str] = mapped_column(String(45))
    avaible: Mapped[int] = mapped_column(Integer)


class Ailog(Base):
    __tablename__ = 'ailog'

    AID: Mapped[int] = mapped_column(Integer, primary_key=True)
    log: Mapped[str] = mapped_column(String(45))


class Class(Base):
    __tablename__ = 'class'

    Class: Mapped[int] = mapped_column(Integer, primary_key=True)
    money_limit: Mapped[str] = mapped_column(String(45))
    creatid: Mapped[str] = mapped_column(String(45))
    createdate: Mapped[str] = mapped_column(String(45))
    modifyid: Mapped[str] = mapped_column(String(45))
    modifydate: Mapped[str] = mapped_column(String(45))
    avaible: Mapped[int] = mapped_column(Integer)


class Othersetting(Base):
    __tablename__ = 'othersetting'

    OID: Mapped[int] = mapped_column(Integer, primary_key=True)
    UID: Mapped[int] = mapped_column(Integer)
    red: Mapped[str] = mapped_column(String(45))
    yellow: Mapped[str] = mapped_column(String(45))
    green: Mapped[str] = mapped_column(String(45))
    mode: Mapped[str] = mapped_column(String(45))


class Ticket(Base):
    __tablename__ = 'ticket'

    TID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Class_: Mapped[int] = mapped_column('Class', Integer)
    UID: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(45))
    status: Mapped[int] = mapped_column(Integer)
    path: Mapped[str] = mapped_column(String(45))
    check_man: Mapped[Optional[str]] = mapped_column(String(45))
    check_date: Mapped[Optional[str]] = mapped_column(String(45))


class TicketDetail(Base):
    __tablename__ = 'ticket_detail'

    td_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    TID: Mapped[str] = mapped_column(String(10))
    time: Mapped[str] = mapped_column(String(45))
    title: Mapped[str] = mapped_column(String(45))
    money: Mapped[Optional[str]] = mapped_column(String(45))


class User(Base):
    __tablename__ = 'user'

    UID: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(45))
    password: Mapped[str] = mapped_column(String(45))
    mail: Mapped[str] = mapped_column(String(45))
    priority: Mapped[int] = mapped_column(Integer)
    img: Mapped[Optional[str]] = mapped_column(String(45))