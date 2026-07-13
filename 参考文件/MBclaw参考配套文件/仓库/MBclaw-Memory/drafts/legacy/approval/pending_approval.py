# 归档自 MBclaw-Lite@d4ea0d26417d5fb2fee0e81c74c331f346221e1b, 路径 app/models/pending_approval.py
# 移出原因：见 MBclaw-Memory/decisions/rejected/ 或 MBclaw/design/audit/SURVIVAL-REVIEW-2026-06-21.md
# R0 状态：移出 Core；R2 重启或永久放弃见上述文档

from sqlalchemy import Column, Integer, String, Text, Float
from app.database import Base


class PendingApproval(Base):
    """Writes that exceed threshold — waiting for user review."""
    __tablename__ = "pending_approvals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    operation = Column(String, default="")
    subsystem = Column(String, default="")
    scope = Column(String, default="")
    origin = Column(String, default="")
    risk_score = Column(Float, default=0.0)
    threshold = Column(Float, default=0.45)
    status = Column(String, default="pending")
    payload_json = Column(Text, default="{}")
    detail = Column(Text, default="")
    created_at = Column(String, default="")
    resolved_at = Column(String, default="")
