from typing import List, Optional


def check_type(type: str) -> str:
    if type == 0:
        return "系統辨識失敗"
    elif type == 1:
        return "等待系統辨識"
    elif type == 2:
        return "傳統發票"
    elif type == 3:
        return "電子發票"
    elif type == 4:
        return "二聯發票"
    elif type == 5:
        return "三聯發票"
    elif type == 6:
        return "收據"


def check_status(status: int) -> str:
    if status == 0:
        return "系統辨識失敗"
    elif status == 1:
        return "等待系統辨識"
    elif status == 2:
        return "待審核"
    elif status == 3:
        return "審核通過"
    elif status == 4:
        return "審核未通過"


def check_mode(mode: Optional[int]) -> Optional[List[int]]:
    if mode is None:
        return None
    elif mode == 0:
        return [1, 2]
    elif mode == 1:
        return [0, 3, 4]
