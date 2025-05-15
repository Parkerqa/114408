from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from model.db_utils import get_db
from model.user_model import get_user
from sqlalchemy.orm import Session
from views.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="無效或過期的 token")
    user = get_user(db, int(payload["sub"]))
    if user is None:
        raise HTTPException(status_code=404, detail="找不到使用者")
    return user

def require_role(*role: int):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.priority not in role:
            raise HTTPException(status_code=403, detail="權限不足")
        return current_user
    return role_checker
