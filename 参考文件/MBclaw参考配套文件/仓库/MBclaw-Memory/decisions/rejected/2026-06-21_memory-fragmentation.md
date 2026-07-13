---
type: rejected
status: archived
decided_by: Claude (CTO memory system design)
verdict: 多种记忆形态并存 → 永久放弃
date: 2026-06-21
---

# 多种记忆形态并存（碎片化反模式）— 永久移出

## 原设计核心
Lite 当前同时存在：
- `memory_store` (MEMORY.md 双态)
- `memory_service` (一般记忆)
- `summary_service` (会话摘要)
- `action_memory_service` (动作记忆)
- `skill_extractor` (SkillCard)
- `classification_service` (树状分类)
- `vector_store` (ChromaDB)
- `layered_search` (L1/L2/L3)
- `dna_service` (Project DNA)

## 否决理由
1. **9 处碎片化** → 任何策略改动需改 9 个文件
2. 互相不一致（有的走 SQLite、有的走文件、有的走 ChromaDB）
3. 组合爆炸 → 测试不可能完整覆盖
4. 维护成本指数增长

## 替代方案（R0 落地）
**唯一 MemoryRepo 抽象**：
```python
class MemoryRepo:
    write_session_memory(sid, summary, keywords, experiences)
    query(q, top_n) -> list[Hit]
    render_injection_for_new_session(exclude_sid) -> str | None
```

承载形态只 2 种：
- **事实记忆**：summaries 表
- **索引记忆**：keywords + messages_fts + experiences_fts

经验沉淀（含失败）统一进 `experiences` 表（`kind ∈ success/failure/lesson`）。

## 教训
> "多种形态各司其职"听起来漂亮，实际是责任分散 + 碎片化。
> MVP 阶段，**唯一抽象 + 唯一存储** 优于"专业分工"。

## 关联
- 架构：[[architecture/ARCH-r0]]
- 风险：survival-review §5 风险 #2
