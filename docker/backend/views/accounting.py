from model.accounting_model import get_account_classes_by_class
from starlette.exceptions import HTTPException


def list_accounting_logic(class_: str):
    if not class_:
        raise HTTPException(status_code=400, detail="請提供 class 參數")

    results = get_account_classes_by_class(class_)
    return "查詢成功", results
