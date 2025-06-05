from pydantic import BaseModel


class ClassUpdate(BaseModel):
    class_: str
    money_limit: str


class ClassCreate(BaseModel):
    class_: str
    money_limit: str
