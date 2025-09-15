from typing import Dict, Optional
from sqlalchemy.orm import Session

from .db_utils import SessionLocal
from .models import OtherSetting


def update_or_insert_theme(user_id: int, theme: int) -> bool:
    db: Session = SessionLocal()
    try:
        setting = db.query(OtherSetting).filter(OtherSetting.user_id == user_id).first()
        if setting:
            setting.theme = theme
        else:
            new_setting = OtherSetting(user_id=user_id, theme=theme)
            db.add(new_setting)

        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()


def update_or_insert_color_setting(user_id: int, payload) -> bool:
    db: Session = SessionLocal()
    try:
        setting = db.query(OtherSetting).filter(OtherSetting.user_id == user_id).first()
        if setting:
            setting.red_bot = payload.red_bot
            setting.red_top = payload.red_top
            setting.yellow_bot = payload.yellow_bot
            setting.yellow_top = payload.yellow_top
            setting.green_bot = payload.green_bot
            setting.green_top = payload.green_top
        else:
            new_setting = OtherSetting(
                user_id=user_id,
                red_bot=payload.red_bot,
                red_top=payload.red_top,
                yellow_bot=payload.yellow_bot,
                yellow_top=payload.yellow_top,
                green_bot=payload.green_bot,
                green_top=payload.green_top,
            )
            db.add(new_setting)

        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()


def get_user_color_setting(user_id: int) -> Optional[Dict]:
    db: Session = SessionLocal()
    try:
        row = (
            db.query(
                OtherSetting.red_bot,
                OtherSetting.red_top,
                OtherSetting.yellow_bot,
                OtherSetting.yellow_top,
                OtherSetting.green_bot,
                OtherSetting.green_top,
            )
            .filter(OtherSetting.user_id == user_id)
            .first()
        )
        if not row:
            return {}
        return {
            "red_bot": int(row.red_bot) if row.red_bot is not None else None,
            "red_top": int(row.red_top) if row.red_top is not None else None,
            "yellow_bot": int(row.yellow_bot) if row.yellow_bot is not None else None,
            "yellow_top": int(row.yellow_top) if row.yellow_top is not None else None,
            "green_bot": int(row.green_bot) if row.green_bot is not None else None,
            "green_top": int(row.green_top) if row.green_top is not None else None,
        }
    except Exception as e:
        print(f"[ERROR] get_user_color_setting failed: {e}")
        return None
    finally:
        db.close()