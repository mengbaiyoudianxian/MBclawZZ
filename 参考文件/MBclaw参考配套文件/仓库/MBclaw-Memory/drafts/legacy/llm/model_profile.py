# 归档自 MBclaw-Lite@d4ea0d26417d5fb2fee0e81c74c331f346221e1b, 路径 app/models/model_profile.py
# 移出原因：见 MBclaw-Memory/decisions/rejected/ 或 MBclaw/design/audit/SURVIVAL-REVIEW-2026-06-21.md
# R0 状态：移出 Core；R2 重启或永久放弃见上述文档

from sqlalchemy import Column, Integer, String, Text, Float
from app.database import Base


class ModelProfile(Base):
    __tablename__ = "model_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key_alias = Column(String, unique=True, nullable=False)
    model_name = Column(String, nullable=False)
    api_base = Column(String, nullable=False, default="")
    capabilities = Column(Text, default="{}")
    strengths = Column(Text, default="[]")
    tool_compatibility = Column(Text, default="{}")
    cost_per_1k_tokens = Column(Float, default=0.0)
    context_window = Column(Integer, default=8192)
    created_at = Column(String, default="")
