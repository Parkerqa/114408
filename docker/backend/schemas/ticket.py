from typing import List, Optional

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TicketDetailUpdate(BaseModel):
    td_id: Optional[int] = None
    title: str
    money: int


class TicketUpdate(BaseModel):
    type: int
    invoice_number: Optional[str] = None
    total_money: int
    Details: List[TicketDetailUpdate]


class TicketList(BaseModel):
    ticket_id: List[int]


class TicketOut(BaseModel):
    ticket_id: int
    time: Optional[datetime]
    type: int
    Details: List[TicketDetailUpdate]
    invoice_number: Optional[str]
    status: int

    model_config = ConfigDict(from_attributes=True)


class TicketAuditItem(BaseModel):
    ticket_id: int = Field(..., description="發票ID")
    status: int = Field(..., description="欲更新的狀態")


class TicketAuditBulkRequest(BaseModel):
    items: List[TicketAuditItem] = Field(..., min_items=1, description="多筆審核項目")