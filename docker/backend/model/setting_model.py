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
            setting.red_but = payload.red_but
            setting.red_top = payload.red_top
            setting.yellow_but = payload.yellow_but
            setting.yellow_top = payload.yellow_top
            setting.green_but = payload.green_but
            setting.green_top = payload.green_top
        else:
            new_setting = OtherSetting(
                uid=uid,
                red_but=payload.red_but,
                red_top=payload.red_top,
                yellow_but=payload.yellow_but,
                yellow_top=payload.yellow_top,
                green_but=payload.green_but,
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