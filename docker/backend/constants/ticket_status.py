from enum import IntEnum

class TicketStatus(IntEnum):
    FAILED = 0            # 系統辨識失敗
    PROCESSING = 1        # 等待系統辨識
    PENDING_REVIEW = 2    # 待審核
    APPROVED = 3          # 審核通過
    REJECTED = 4          # 審核未通過

# 哪些狀態視為「完成態」= 不可再被修改
FINAL_STATES = {TicketStatus.APPROVED, TicketStatus.REJECTED}