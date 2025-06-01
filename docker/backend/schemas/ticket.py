from typing import List, Optional

from pydantic import BaseModel


class TicketDetailUpdate(BaseModel):
    id: Optional[int] = None
    title: str
    money: str

class TicketUpdate(BaseModel):
    detail: List[TicketDetailUpdate]

class TicketAuditRequest(BaseModel):
    status: int