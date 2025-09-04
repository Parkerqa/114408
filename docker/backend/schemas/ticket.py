from typing import List, Optional

from pydantic import BaseModel, Field


class TicketDetailUpdate(BaseModel):
    id: Optional[int] = None
    title: str
    money: str


class TicketUpdate(BaseModel):
    detail: List[TicketDetailUpdate]


class TicketAuditItem(BaseModel):
    ticket_id: int = Field(..., description="發票ID")
    status: int = Field(..., description="欲更新的狀態（例：0=待審、1=退回、2=通過）")

class TicketAuditBulkRequest(BaseModel):
    items: List[TicketAuditItem] = Field(..., min_items=1, description="多筆審核項目")