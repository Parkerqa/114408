from sqlalchemy.orm import Session

from model.db_utils import SessionLocal
from model.models import User


# dependencies.py
def get_user(db: Session, uid: int):
    try:
        return db.query(User).filter(User.uid == uid).one_or_none()
    except Exception as e:
        print(f"[ERROR] get_user: {e}")
        return None


# 給 views 使用的查詢函式
def get_user_by_email(email: str):
    db: Session = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).one_or_none()
    except Exception as e:
        print(f"[ERROR] get_user_by_email: {e}")
        return None
    finally:
        db.close()

# 建立使用者
def create_user(username: str, email: str, password: str):
    db: Session = SessionLocal()
    try:
        user = User(username=username, email=email, password=password, priority=0)
        db.add(user)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[ERROR] create_user: {e}")
        return False
    finally:
        db.close()

# 更新密碼
def update_password(email: str, new_pwd: str):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).one_or_none()
        if not user:
            return False
        user.password = new_pwd
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[ERROR] update_password: {e}")
        return False
    finally:
        db.close()

# 更新使用者資料
def update_user_info(uid: int, username: str, email: str, password: str):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.uid == uid).one_or_none()
        if not user:
            return False
        user.username = username
        user.email = email
        user.password = password
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[ERROR] update_user_info: {e}")
        return False
    finally:
        db.close()

# 給 views 使用的查詢函式
def get_user_by_uid(uid: int):
    db: Session = SessionLocal()
    try:
        return db.query(User).filter(User.uid == uid).one_or_none()
    except Exception as e:
        print(f"[ERROR] get_user_by_uid: {e}")
        return None
    finally:
        db.close()

# 更新使用者頭像
def update_user_img(uid: int, filename: str):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.uid == uid).one_or_none()
        if not user:
            return False
        user.img = filename
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[ERROR] update_user_img: {e}")
        return False
    finally:
        db.close()
