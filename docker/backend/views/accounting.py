from model.accounting_model import get_account_classes_by_class


def list_accounting_logic(class_: str):
    try:
        if not class_:
            return "請提供 class 參數", "error", 400, None

        results = get_account_classes_by_class(class_)
        return "查詢成功", "success", 200, results

    except Exception as e:
        print(f"[ERROR] 查詢 account_class 發生錯誤：{e}")
        return "伺服器錯誤", "error", 500, None
