# 归档自 MBclaw-Lite@d4ea0d26417d5fb2fee0e81c74c331f346221e1b, 路径 app/models/external_integration.py
# 移出原因：见 MBclaw-Memory/decisions/rejected/ 或 MBclaw/design/audit/SURVIVAL-REVIEW-2026-06-21.md
# R0 状态：移出 Core；R2 重启或永久放弃见上述文档

from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class ExternalIntegration(Base):
    __tablename__ = "external_integrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider = Column(String, nullable=False)
    display_name = Column(String, default="")
    api_key = Column(Text, default="")
    base_url = Column(String, default="")
    config = Column(Text, default="{}")
    status = Column(String, default="inactive")
    free_trial_expiry = Column(String, default="")
    created_at = Column(String, default="")
    updated_at = Column(String, default="")
