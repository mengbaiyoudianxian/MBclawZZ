# 归档自 MBclaw-Lite@d4ea0d26417d5fb2fee0e81c74c331f346221e1b, 路径 app/models/tool.py
# 移出原因：见 MBclaw-Memory/decisions/rejected/ 或 MBclaw/design/audit/SURVIVAL-REVIEW-2026-06-21.md
# R0 状态：移出 Core；R2 重启或永久放弃见上述文档

from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from app.database import Base


class ToolRegistry(Base):
    __tablename__ = "tool_registry"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    summary_100 = Column(String(200), nullable=False, default="")
    tags = Column(Text, default="[]")
    full_description = Column(Text, default="")
    usage_examples = Column(Text, default="[]")
    compatible_models = Column(Text, default="[]")
    classification_node_id = Column(Integer, nullable=True)
    embedding_text = Column(Text, default="")
    rating = Column(Float, default=0.0)
    usage_count = Column(Integer, default=0)
    created_at = Column(String, default="")
    updated_at = Column(String, default="")
