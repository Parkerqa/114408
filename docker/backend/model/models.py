import decimal
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy import (CHAR, DECIMAL, Boolean, DateTime, Enum, ForeignKey,
                        Integer, String, Text, func)
from sqlalchemy.dialects.mysql import DATETIME, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

TW_TZ = timezone(timedelta(hours=8))


def now_tw():
    return datetime.now(TW_TZ)


class Base(DeclarativeBase):
    pass


class Accounting(Base):
    __tablename__ = 'accounting'

    accounting_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_info_id: Mapped[str] = mapped_column(Enum('傳統', '1'))

    create_id: Mapped[Optional[str]] = mapped_column(String(150))
    create_date: Mapped[Optional[datetime]] = mapped_column(DATETIME(fsp=6), default=now_tw)

    modify_id: Mapped[Optional[str]] = mapped_column(String(150))
    modify_date: Mapped[Optional[datetime]] = mapped_column(DATETIME(fsp=6), default=now_tw, onupdate=now_tw)

    avaible: Mapped[int] = mapped_column(TINYINT)
    account_class: Mapped[Optional[str]] = mapped_column(String(150))


class AiLog(Base):
    __tablename__ = 'ai_log'

    ai_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    log: Mapped[str] = mapped_column(Text)
    create_id: Mapped[str] = mapped_column(String(150))
    create_date: Mapped[datetime] = mapped_column(DATETIME(fsp=6))


class ClassInfo(Base):
    __tablename__ = 'class_info'

    class_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    money_limit: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2))
    class_info_id: Mapped[str] = mapped_column(Enum('交通'))

    create_id: Mapped[Optional[str]] = mapped_column(String(150))
    create_date: Mapped[Optional[datetime]] = mapped_column(DATETIME(fsp=6), default=now_tw)

    modify_id: Mapped[Optional[str]] = mapped_column(String(150))
    modify_date: Mapped[Optional[datetime]] = mapped_column(DATETIME(fsp=6), default=now_tw, onupdate=now_tw)

    available: Mapped[int] = mapped_column(TINYINT)


class OtherSetting(Base):
    __tablename__ = 'other_setting'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    theme: Mapped[int] = mapped_column(Integer)
    red_bot: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2))
    red_top: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2))
    green_bot: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2))
    green_top: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2))
    yellow_bot: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2))
    yellow_top: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2))


class Request(Base):
    __tablename__ = 'request'

    request_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mappping: Mapped[str] = mapped_column(CHAR(45))
    user_agent: Mapped[str] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(String(255))
    open_file_path: Mapped[str] = mapped_column(String(255))
    http_status_code: Mapped[str] = mapped_column(CHAR(45))
    request_ip_from: Mapped[str] = mapped_column(String(150))
    priority: Mapped[int] = mapped_column(TINYINT)
    request_time: Mapped[datetime] = mapped_column(DateTime)


class Ticket(Base):
    __tablename__ = 'ticket'

    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[Optional[int]] = mapped_column(Integer)
    invoice_number: Mapped[Optional[str]] = mapped_column(String(10))
    class_info_id: Mapped[Optional[str]] = mapped_column(Enum('a'))
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    check_man: Mapped[Optional[str]] = mapped_column(String(150))
    check_date: Mapped[Optional[datetime]] = mapped_column(DATETIME(fsp=6))
    img: Mapped[Optional[str]] = mapped_column(String(255))
    date: Mapped[Optional[datetime]] = mapped_column(DATETIME(fsp=6))
    total_money: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    status: Mapped[Optional[int]] = mapped_column(Integer)

    create_id: Mapped[Optional[str]] = mapped_column(String(150))
    create_date: Mapped[Optional[datetime]] = mapped_column(DATETIME(fsp=6), default=now_tw)

    modify_id: Mapped[Optional[str]] = mapped_column(String(150))
    modify_date: Mapped[Optional[datetime]] = mapped_column(DATETIME(fsp=6), default=now_tw, onupdate=now_tw)

    available: Mapped[Optional[int]] = mapped_column(TINYINT)
    writeoff_date: Mapped[Optional[datetime]] = mapped_column(DATETIME(fsp=6))

    ticket_details: Mapped[List["TicketDetail"]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan"
    )


class TicketDetail(Base):
    __tablename__ = 'ticket_detail'

    td_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(Integer, ForeignKey('ticket.ticket_id', ondelete='CASCADE'), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(128))
    money: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))

    ticket: Mapped["Ticket"] = relationship(back_populates="ticket_details")


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(254))
    password: Mapped[str] = mapped_column(String(128))
    username: Mapped[Optional[str]] = mapped_column(String(150))
    priority: Mapped[Optional[int]] = mapped_column(Integer)
    img: Mapped[Optional[str]] = mapped_column(String(255))

    create_id: Mapped[Optional[str]] = mapped_column(String(150))
    create_date: Mapped[Optional[datetime]] = mapped_column(DATETIME(fsp=6), default=now_tw)

    modify_id: Mapped[Optional[str]] = mapped_column(String(150))
    modify_date: Mapped[Optional[datetime]] = mapped_column(DATETIME(fsp=6), default=now_tw, onupdate=now_tw)

    available: Mapped[Optional[int]] = mapped_column(TINYINT)
