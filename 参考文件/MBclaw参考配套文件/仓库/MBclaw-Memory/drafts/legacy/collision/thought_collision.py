# 归档自 MBclaw-Lite@d4ea0d26417d5fb2fee0e81c74c331f346221e1b, 路径 app/models/thought_collision.py
# 移出原因：见 MBclaw-Memory/decisions/rejected/ 或 MBclaw/design/audit/SURVIVAL-REVIEW-2026-06-21.md
# R0 状态：移出 Core；R2 重启或永久放弃见上述文档

"""Project 14: Thought Collision — combinatorial innovation from existing knowledge.

Randomly selects successful memories, user-praised skills, and proven approaches,
then generates novel combinations that may produce unexpected synergies (奇效).

These combinations are preserved and prioritized in future project contexts.
"""

from sqlalchemy import Column, Integer, String, Text, Float
from app.database import Base


class ThoughtCollision(Base):
    """A novel combination of existing memories/skills/approaches."""
    __tablename__ = "thought_collisions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)

    # Input ingredients
    memory_snippets = Column(Text, default="[]")     # JSON: list of memory entries used
    skill_ids = Column(Text, default="[]")            # JSON: list of skill_card IDs used
    approach_names = Column(Text, default="[]")       # JSON: list of approach names used

    # Synthesis
    combo_name = Column(String, default="")           # human-readable name
    combo_description = Column(Text, default="")      # what this combination does
    expected_synergy = Column(Text, default="")       # why these pieces work together
    synergy_score = Column(Float, default=0.0)        # 0-1: how promising is this

    # Status and testing
    status = Column(String, default="proposed")       # proposed → tested → proven / discarded
    tested_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    last_tested_at = Column(String, default="")
    last_result = Column(Text, default="")

    # Priority boost for future sessions
    priority_boost = Column(Float, default=0.0)       # added to relevance score in bootstrap

    created_at = Column(String, default="")

    @property
    def success_rate(self) -> float:
        return self.success_count / self.tested_count if self.tested_count > 0 else 0.0
