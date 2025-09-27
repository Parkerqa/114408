from typing import List

from pydantic import BaseModel, condecimal


class DepartmentCreate(BaseModel):
    name: str
    money_limit: int


class DepartmentUpdate(BaseModel):
    name: str
    money_limit: int


class DepartmentAccountingUpdateItem(BaseModel):
    accounting_id: int
    budget_limit: float


class DepartmentAccountingSync(BaseModel):
    accounting_items: List[DepartmentAccountingUpdateItem]