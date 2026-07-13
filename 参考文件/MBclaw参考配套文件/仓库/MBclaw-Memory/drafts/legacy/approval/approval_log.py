# 归档自 MBclaw-Lite@d4ea0d26417d5fb2fee0e81c74c331f346221e1b, 路径 app/models/approval_log.py
# 移出原因：见 MBclaw-Memory/decisions/rejected/ 或 MBclaw/design/audit/SURVIVAL-REVIEW-2026-06-21.md
# R0 状态：移出 Core；R2 重启或永久放弃见上述文档

from sqlalchemy import Column, Integer, String, Text, Float
from app.database import Base


class ApprovalLog(Base):
    """Auto-approved writes — transparent audit trail."""
    __tablename__ = "approval_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    operation = Column(String, default="")
    subsystem = Column(String, default="")
    scope = Column(String, default="")
    origin = Column(String, default="")
    risk_score = Column(Float, default=0.0)
    threshold = Column(Float, default=0.45)
    decision = Column(String, default="auto_approved")
    detail = Column(Text, default="")
    created_at = Column(String, default="")
