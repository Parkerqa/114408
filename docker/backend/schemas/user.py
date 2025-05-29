from typing import Optional

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

class ModifyUserInfo(BaseModel):
    username: str
    email: EmailStr
    new_password: Optional[str] = None  # 若提供才改密碼