# 归档自 MBclaw-Lite@d4ea0d26417d5fb2fee0e81c74c331f346221e1b, 路径 app/models/classification_node.py
# 移出原因：见 MBclaw-Memory/decisions/rejected/ 或 MBclaw/design/audit/SURVIVAL-REVIEW-2026-06-21.md
# R0 状态：移出 Core；R2 重启或永久放弃见上述文档

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ClassificationNode(Base):
    __tablename__ = "classification_nodes"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("classification_nodes.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)
    level = Column(Integer, nullable=False, default=1)
    category_name = Column(String(256), nullable=False)
    summary_short = Column(Text, default="")
    summary_detailed = Column(Text, default="")
    failed_approaches = Column(Text, default="[]")
    keywords = Column(Text, default="[]")
    embedding_json = Column(Text, default="")

    session = relationship("Session", back_populates="classification_nodes")
