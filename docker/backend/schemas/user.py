from typing import Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, EmailStr


# user base
class UserBase(BaseModel):
    username: str
    email: EmailStr


# register
class UserCreate(UserBase):
    password: str


# login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# forget password
class PasswordForget(BaseModel):
    email: EmailStr


class HashIn(BaseModel):
    password: str


class ModifyUserInfo(BaseModel):
    username: str
    email: EmailStr
    new_password: Optional[str] = None  # 若提供才改密碼


def ModifyUserInfoForm(
        username: str = Form(...),
        email: EmailStr = Form(...),
        new_password: Optional[str] = Form(None),
        avatar: Optional[UploadFile] = File(None)
):
    data = ModifyUserInfo(
        username=username,
        email=email,
        new_password=new_password
    )
    return data, avatar
