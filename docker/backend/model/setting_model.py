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
            setting.red_usage_rate = payload.red_usage_rate
            setting.red_remaining_rate = payload.red_remaining_rate
            setting.yellow_usage_rate = payload.yellow_usage_rate
            setting.yellow_remaining_rate = payload.yellow_remaining_rate
            setting.green_usage_rate = payload.green_usage_rate
            setting.green_remaining_rate = payload.green_remaining_rate
        else:
            new_setting = OtherSetting(
                user_id=user_id,
                red_bot=payload.red_usage_rate,
                red_top=payload.red_remaining_rate,
                yellow_bot=payload.yellow_usage_rate,
                yellow_top=payload.yellow_remaining_rate,
                green_bot=payload.green_usage_rate,
                green_top=payload.green_remaining_rate,
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
                OtherSetting.red_usage_rate,
                OtherSetting.red_remaining_rate,
                OtherSetting.yellow_usage_rate,
                OtherSetting.yellow_remaining_rate,
                OtherSetting.green_usage_rate,
                OtherSetting.green_remaining_rate,
            )
            .filter(OtherSetting.user_id == user_id)
            .first()
        )
        if not row:
            return {}
        return {
            "red_usage_rate": int(row.red_usage_rate) if row.red_usage_rate is not None else None,
            "red_remaining_rate": int(row.red_remaining_rate) if row.red_remaining_rate is not None else None,
            "yellow_usage_rate": int(row.yellow_usage_rate) if row.yellow_usage_rate is not None else None,
            "yellow_remaining_rate": int(row.yellow_remaining_rate) if row.yellow_remaining_rate is not None else None,
            "green_usage_rate": int(row.green_usage_rate) if row.green_usage_rate is not None else None,
            "green_remaining_rate": int(row.green_remaining_rate) if row.green_remaining_rate is not None else None,
        }
    except Exception as e:
        print(f"[ERROR] get_user_color_setting failed: {e}")
        return None
    finally:
        db.close()