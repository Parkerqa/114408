from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime
from .db_utils import SessionLocal
from .models import Ticket, TicketDetail


def save_error(ticket_id):
    db: SessionLocal = SessionLocal()
    try:
        db.query(Ticket).filter(Ticket.ticket_id == ticket_id).update({
            Ticket.type: 0,
            Ticket.status: 0
        })
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    finally:
        db.close()


def _to_int(x):
    try:
        if x is None:
            return None
        s = str(x).replace(",", "").strip()
        return int(float(s))
    except Exception:
        return None


def normalize_catch_result(catch_result: dict) -> dict:
    """
    接受多種輸入結構：
    A) 扁平：
       {"invoice_number": "...", "date": "...", "total_money": 123,
        "title": [...], "money": [...]}

    B) 巢狀：
       {"ticket": {"invoice_number": "...", "date": "...", "total_money": 123},
        "ticket_detail": [{"title":"A","money":50}, ...]}

    C) 容錯別名：
       invoice_no / invoiceNum / number
       total / total_amount / amount / totalMoney
    """
    if not isinstance(catch_result, dict):
        raise ValueError("catch_result 應為 dict")

    # 先從扁平抓
    inv = catch_result.get("invoice_number") or catch_result.get("invoice_no") or \
          catch_result.get("invoiceNum") or catch_result.get("number")
    dt  = catch_result.get("date")
    tot = catch_result.get("total_money") or catch_result.get("total") or \
          catch_result.get("total_amount") or catch_result.get("amount") or \
          catch_result.get("totalMoney")

    titles = catch_result.get("title")
    moneys = catch_result.get("money")

    # 如果有 ticket/ticket_detail，用它覆蓋
    ticket = catch_result.get("ticket") or {}
    if isinstance(ticket, dict):
        inv = ticket.get("invoice_number") or inv
        dt  = ticket.get("date") or dt
        tot = ticket.get("total_money") or tot

    details = catch_result.get("ticket_detail")
    if isinstance(details, list) and details:
        titles = [d.get("title") for d in details if isinstance(d, dict)]
        moneys = [d.get("money") for d in details if isinstance(d, dict)]

    # 轉型 & 清洗
    if isinstance(moneys, list):
        moneys = [_to_int(x) for x in moneys]
    if isinstance(tot, (str, int, float)):
        tot = _to_int(tot)

    # 保證長度一致
    if isinstance(titles, list) and isinstance(moneys, list):
        if len(titles) != len(moneys):
            n = min(len(titles), len(moneys))
            titles = titles[:n]
            moneys = moneys[:n]

    return {
        "invoice_number": inv,
        "date": dt,
        "total_money": tot,
        "title": titles or [],
        "money": moneys or []
    }


# save ocr output
def save_ocr_result(ticket_id, invoice_type, catch_result):
    db: Session = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).one_or_none()
        if not ticket:
            return False

        # 先正規化
        norm = normalize_catch_result(catch_result)

        ticket.type = invoice_type
        ticket.invoice_number = norm.get("invoice_number")
        ticket.date = norm.get("date")
        ticket.total_money = norm.get("total_money")
        ticket.status = 2
        ticket.updated_by = 0

        # 先刪舊的明細（避免重複）
        db.query(TicketDetail).filter(TicketDetail.ticket_id == ticket_id).delete()

        titles = norm.get("title", []) or []
        moneys = norm.get("money", []) or []

        # 僅保留 title 有內容且 money 為數字的
        details = []
        for t, m in zip(titles, moneys):
            if t and (m is not None):
                details.append(TicketDetail(ticket_id=ticket_id, title=t, money=m))

        if details:
            db.add_all(details)

        db.commit()
        return True

    except Exception as e:
        print(f"[ERROR] 儲存 OCR 結果失敗：{e}")
        db.rollback()
        return False
    finally:
        db.close()


# save qrcode decoder output
def save_qrcode_result(ticket_id, invoice_type, catch_result, items):
    db: Session = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).one_or_none()
        ticket.type = invoice_type
        ticket.invoice_number = catch_result["invoice_number"]
        ticket.date = catch_result["date"]
        ticket.total_money = catch_result["total_money"]
        ticket.status = 2
        ticket.updated_by = 0

        for item in items:
            detail = TicketDetail(
                ticket_id=ticket_id,
                title=item["title"],
                money=item["money"]
            )
            db.add(detail)
        db.commit()
        return True
    except Exception as e:
        print(f"[ERROR] 儲存 QRcode Decorder 結果失敗：{e}")
        db.rollback()
        return False
    finally:
        db.close()


def _normalize_n8n_response(n8n_resp):
    """
    將 n8n 回應統一成：
    {
      "ticket": {"invoice_number": str, "date": str, "total_money": number},
      "ticket_detail": [{"title": str, "money": number}, ...]
    }
    """
    if n8n_resp is None:
        return None
    # n8n 目前回傳是 [ { "ticket": {...}, "ticket_detail": [...] } ]
    if isinstance(n8n_resp, list):
        n8n_resp = n8n_resp[0] if n8n_resp else None
    if not isinstance(n8n_resp, dict):
        return None

    ticket = n8n_resp.get("ticket", {}) or {}
    details = n8n_resp.get("ticket_detail", []) or []

    return {
        "ticket": {
            "invoice_number": ticket.get("invoice_number"),
            "date": ticket.get("date"),
            "total_money": ticket.get("total_money"),
        },
        "ticket_detail": details,
    }

def _parse_dt(dt_str):
    """
    嘗試解析多種常見格式；失敗回傳 None。
    """
    if not dt_str:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d", "%Y/%m/%d %H:%M:%S"):
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue
    return None

def update_ticket_from_n8n(ticket_id, n8n_resp):
    db: Session = SessionLocal()
    try:
        payload = _normalize_n8n_response(n8n_resp)
        if not payload:
            print("[WARN] n8n 回應為空或格式不符，略過更新。")
            return False

        t = payload["ticket"]
        details = payload["ticket_detail"]

        ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).one_or_none()
        if ticket is None:
            print(f"[ERROR] 找不到 ticket_id={ticket_id} 的票據。")
            return False

        # === 更新主表欄位（有值才更新；避免覆蓋成 None） ===
        if t.get("invoice_number"):
            ticket.invoice_number = t["invoice_number"]

        if t.get("date") is not None:
            parsed = _parse_dt(t["date"])
            # 依你的模型欄位型別選擇：若 Ticket.date 是 DATE，可用 parsed.date()
            # 若是 DATETIME 就用 parsed；如果解析失敗就不更新
            if parsed:
                # 假設欄位是 DATETIME；若是 DATE 請改成 parsed.date()
                ticket.date = parsed

        if t.get("total_money") is not None:
            ticket.total_money = t["total_money"]

        ticket.updated_by = "system"

        # === 覆蓋明細：先刪舊後加新，避免重複 ===
        db.query(TicketDetail).filter(TicketDetail.ticket_id == ticket_id).delete(synchronize_session=False)

        # details 可能是空陣列；這樣等於清空明細
        for item in details:
            title = item.get("title")
            money = item.get("money")
            if title is None and money is None:
                continue  # 全空就跳過
            db.add(TicketDetail(
                ticket_id=ticket_id,
                title=title,
                money=money
            ))

        db.commit()
        return True

    except SQLAlchemyError as e:
        print(f"[ERROR] 儲存 N8N 結果失敗（DB）：{e}")
        db.rollback()
        return False
    except Exception as e:
        print(f"[ERROR] 儲存 N8N 結果失敗（程式）：{e}")
        db.rollback()
        return False
    finally:
        db.close()