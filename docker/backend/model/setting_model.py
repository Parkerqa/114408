from sqlalchemy.orm import Session

from .db_utils import SessionLocal
from .models import OtherSetting


def update_or_insert_theme(uid: int, theme: int) -> bool:
    db: Session = SessionLocal()
    try:
        setting = db.query(OtherSetting).filter(OtherSetting.uid == uid).first()
        if setting:
            setting.theme = theme
        else:
            new_setting = OtherSetting(uid=uid, theme=theme)
            db.add(new_setting)

        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()

def update_or_insert_color_setting(uid: int, payload) -> bool:
    db: Session = SessionLocal()
    try:
        setting = db.query(OtherSetting).filter(OtherSetting.uid == uid).first()
        if setting:
            setting.red_bot = payload.red_bot
            setting.red_top = payload.red_top
            setting.yellow_bot = payload.yellow_bot
            setting.yellow_top = payload.yellow_top
            setting.green_bot = payload.green_bot
            setting.green_top = payload.green_top
        else:
            new_setting = OtherSetting(
                uid=uid,
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