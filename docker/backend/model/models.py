from typing import Optional, List
import datetime
import decimal

from sqlalchemy import BigInteger, CHAR, Column, DECIMAL, DateTime, Enum, ForeignKeyConstraint, Index, Integer, String, Table, Text, text, ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.mysql import DATETIME, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class AccountingItems(Base):
    __tablename__ = 'accounting_items'
    __table_args__ = (
        Index('uk_accounting_code', 'account_code', unique=True),
    )

    accounting_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    account_code: Mapped[str] = mapped_column(String(50), nullable=False)
    account_name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    created_by: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    account_class: Mapped[Optional[str]] = mapped_column(String(150))
    updated_by: Mapped[Optional[str]] = mapped_column(String(150))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    department_accounting: Mapped[list['DepartmentAccounting']] = relationship('DepartmentAccounting', back_populates='accounting')


class AiLog(Base):
    __tablename__ = 'ai_log'

    ai_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    log: Mapped[str] = mapped_column(Text, nullable=False)
    created_by: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False, server_default=text('CURRENT_TIMESTAMP(6)'))


class Departments(Base):
    __tablename__ = 'departments'
    __table_args__ = (
        Index('uk_departments_code', 'dept_code', unique=True),
    )

    department_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    dept_code: Mapped[str] = mapped_column(String(50), nullable=False)
    dept_name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    created_by: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    updated_by: Mapped[Optional[str]] = mapped_column(String(150))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    department_accounting: Mapped[list['DepartmentAccounting']] = relationship('DepartmentAccounting', back_populates='department')


class OtherSetting(Base):
    __tablename__ = 'other_setting'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    theme: Mapped[int] = mapped_column(Integer, nullable=False)
    red_usage_rate: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    red_remaining_rate: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    green_usage_rate: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    green_remaining_rate: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    yellow_usage_rate: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    yellow_remaining_rate: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)


t_request = Table(
    'request', Base.metadata,
    Column('mappping', CHAR(45), nullable=False),
    Column('user_agent', String(255), nullable=False),
    Column('url', String(255), nullable=False),
    Column('open_file_path', String(255), nullable=False),
    Column('http_status_code', CHAR(45), nullable=False),
    Column('request_ip_from', String(150), nullable=False),
    Column('priority', TINYINT, nullable=False),
    Column('request_time', DateTime, nullable=False)
)


class Ticket(Base):
    __tablename__ = 'ticket'

    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    created_by: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False, server_default=text('CURRENT_TIMESTAMP(6)'))
    type: Mapped[Optional[int]] = mapped_column(Integer)
    invoice_number: Mapped[Optional[str]] = mapped_column(String(10))
    class_info_id: Mapped[Optional[str]] = mapped_column(Enum('a'))

    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user.user_id", ondelete="SET NULL"),
        index=True,
        nullable=True
    )

    check_man: Mapped[Optional[str]] = mapped_column(String(150))
    check_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    img: Mapped[Optional[str]] = mapped_column(String(255))
    date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    total_money: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    status: Mapped[Optional[int]] = mapped_column(Integer)
    writeoff_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_by: Mapped[Optional[str]] = mapped_column(String(150))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))

    user: Mapped["User"] = relationship(
        "User",
        back_populates="tickets",
        foreign_keys=[user_id],
        lazy="joined",
    )

    ticket_detail: Mapped[List["TicketDetail"]] = relationship(
        'TicketDetail',
        back_populates='ticket',
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    created_by: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False, server_default=text('CURRENT_TIMESTAMP(6)'))
    username: Mapped[Optional[str]] = mapped_column(String(150))
    priority: Mapped[Optional[int]] = mapped_column(Integer)
    img: Mapped[Optional[str]] = mapped_column(String(255))
    updated_by: Mapped[Optional[str]] = mapped_column(String(150))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME(fsp=6),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP(6)"),
        server_onupdate=text("CURRENT_TIMESTAMP(6)")
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket",
        back_populates="user",
        foreign_keys="Ticket.user_id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class DepartmentAccounting(Base):
    __tablename__ = 'department_accounting'
    __table_args__ = (
        ForeignKeyConstraint(['accounting_id'], ['accounting_items.accounting_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_da_accounting'),
        ForeignKeyConstraint(['department_id'], ['departments.department_id'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_da_department'),
        Index('fk_da_accounting', 'accounting_id'),
        Index('uk_da', 'department_id', 'accounting_id', unique=True)
    )

    dept_accounting_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    department_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    accounting_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    budget_limit: Mapped[decimal.Decimal] = mapped_column(DECIMAL(12, 2), nullable=False, server_default=text("'0.00'"))
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    created_by: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_by: Mapped[Optional[str]] = mapped_column(String(150))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    accounting: Mapped['AccountingItems'] = relationship('AccountingItems', back_populates='department_accounting')
    department: Mapped['Departments'] = relationship('Departments', back_populates='department_accounting')


class TicketDetail(Base):
    __tablename__ = 'ticket_detail'
    __table_args__ = (
        ForeignKeyConstraint(
            ['ticket_id'], ['ticket.ticket_id'],
            ondelete='CASCADE',
            name='fk_ticket_detail_ticket'
        ),
        Index('ix_ticket_detail_ticket_id', 'ticket_id'),
    )

    td_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticket_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(128))
    money: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))

    ticket: Mapped["Ticket"] = relationship('Ticket', back_populates='ticket_detail')
