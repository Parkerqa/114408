from typing import Optional

from model.db_utils import SessionLocal
from model.models import OtherSetting, User
from sqlalchemy.orm import Session, aliased


# dependencies.py
def get_user(db: Session, user_id: int) -> Optional[User]:
    try:
        return db.query(User).filter(User.user_id == user_id).one_or_none()
    except Exception as e:
        print(f"[ERROR] get_user: {e}")
        return None


# 給 views 使用的查詢函式
def get_user_by_email(email: str) -> Optional[User]:
    db: Session = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).one_or_none()
    except Exception as e:
        print(f"[ERROR] get_user_by_email: {e}")
        return None
    finally:
        db.close()

# 建立使用者
def create_user(username: str, email: str, password: str) -> bool:
    db: Session = SessionLocal()
    try:
        user = User(username=username, email=email, password=password, priority=0, img="user.png", available=True)
        db.add(user)
        db.commit()

        user.create_id = user.user_id
        user.modify_id = user.user_id
        other_setting = OtherSetting(user_id=user.user_id, theme=0,
                                     red_bot=0, red_top=50,
                                     green_bot=51, green_top=70,
                                     yellow_bot=71, yellow_top=100)
        db.add(other_setting)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[ERROR] create_user: {e}")
        return False
    finally:
        db.close()

# 更新密碼
def update_password(email: str, new_pwd: str) -> bool:
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
def update_user_info(user_id: int, username: str, email: str, password: str, img: str) -> bool:
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).one_or_none()
        if not user:
            return False
        user.username = username
        user.email = email
        user.password = password
        user.img = img
        user.modify_id = user_id
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[ERROR] update_user_info: {e}")
        return False
    finally:
        db.close()

# 給 views 使用的查詢函式
def get_user_by_uid(user_id: int) -> Optional[User]:
    db: Session = SessionLocal()
    try:
        return db.query(User).filter(User.user_id == user_id).one_or_none()
    except Exception as e:
        print(f"[ERROR] get_user_by_user_id: {e}")
        return None
    finally:
        db.close()


def get_user_settings(user_id: int):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).one_or_none()
        if not user:
            return None
        user = aliased(User)
        settings = aliased(OtherSetting)
        return db.query(user.priority, settings.theme)\
            .outerjoin(settings, user.user_id == settings.user_id)\
            .filter(user.user_id == user_id)\
            .one_or_none()
    except Exception as e:
        print(f"[ERROR] get_user_settings: {e}")
        return None
    finally:
        db.close()