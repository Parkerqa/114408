from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# user base
class UserBase(BaseModel):
    username: str
    email: EmailStr

# userinfo send to frontend
class UserOut(BaseModel):
    uid: int
    username: str
    email: EmailStr
    priority: Optional[int] = None
    img: Optional[str] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)


# register
class UserCreate(UserBase):
    password: str

# login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(UserOut):
    password: str

# update password
class PasswordChange(BaseModel):
    old_password: str
    new_password: str

# forget password
class PasswordForget(BaseModel):
    email: EmailStr

class ModifyUserInfo(BaseModel):
    username: str
    email: EmailStr
    old_password: str
    new_password: Optional[str] = None  # 若提供才改密碼