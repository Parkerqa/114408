import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000
FORGET_PASSWORD_TOKEN_EXPIRE_MINUTES = 3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# plain to hash
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# verify user
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# create JWT
def create_access_token(user_id: int, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    tzone = timezone(timedelta(hours=8))
    expire = datetime.now(tz=tzone) + timedelta(minutes=expires_minutes)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# check current JWT
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "sub" not in payload:
            return None
        return payload
    except JWTError:
        return None
