from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str
    money_limit: int


class DepartmentUpdate(BaseModel):
    name: str
    money_limit: int