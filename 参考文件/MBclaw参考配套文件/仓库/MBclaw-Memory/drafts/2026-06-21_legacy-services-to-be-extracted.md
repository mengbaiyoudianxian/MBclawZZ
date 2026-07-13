---
type: draft
status: extracted
decided_by: Claude (CTO audit)
verdict: R0 期内由 OpenHands 物理迁出 Core
date: 2026-06-21
---

# 待物理迁出 Core 的 services 清单

R0 阶段任务：以下文件**保留代码**但从 Core 主分支移出，归档到本仓库 `drafts/legacy/<file>.py`。

| 源文件 (MBclaw-Lite) | 行数 | 归档目录 | 处置 |
|---|---|---|---|
| `app/services/utopia_service.py` | 382 | `drafts/legacy/utopia/` | 永久移出 |
| `app/services/chat_extractor.py` | 387 | `drafts/legacy/utopia/` | 永久移出 |
| `app/services/psychology_engine.py` | 333 | `drafts/legacy/psychology/` | 永久移出 |
| `app/services/collision_engine.py` | 272 | `drafts/legacy/collision/` | 永久移出 |
| `app/services/sub_agent_coordinator.py` | 131 | `drafts/legacy/agent/` | 永久移出 |
| `app/services/dual_key.py` | 96 | `drafts/legacy/agent/` | 永久移出 |
| `app/services/agent_runtime.py` | 438 | `drafts/legacy/agent/` | R2 重写参考 |
| `app/services/skill_extractor.py` | 350 | `drafts/legacy/agent/` | R2 重写参考 |
| `app/services/curator.py` | 123 | `drafts/legacy/agent/` | R2 重写参考 |
| `app/services/feedback_service.py` | 141 | `drafts/legacy/feedback/` | R2 重写参考 |
| `app/services/classification_service.py` | 204 | `drafts/legacy/classification/` | R2 重写参考 |
| `app/services/vector_store.py` | ? | `drafts/legacy/vector/` | R2 重写参考 |
| `app/services/layered_search.py` | 143 | `drafts/legacy/search/` | 合并入新 search |
| `app/services/integration_service.py` | 154 | `drafts/legacy/integrations/` | R3 重启参考 |
| `app/services/i18n_service.py` | 118 | `drafts/legacy/i18n/` | R3 重启参考 |
| `app/services/approval_gate.py` | 302 | `drafts/legacy/approval/` | 简化版进 R1 memory_store |
| `app/services/task_queue.py` | 138 | `drafts/legacy/queue/` | R2 重启参考 |
| `app/services/message_priority.py` | ? | `drafts/legacy/queue/` | R2 重启参考 |
| `app/services/auto_mode.py` | 103 | `drafts/legacy/agent/` | R2 重写参考 |
| `app/services/tool_service.py` | 141 | `drafts/legacy/tools/` | R2 重启参考 |
| `app/services/model_service.py` | 93 | `drafts/legacy/llm/` | R2 重启参考 |
| `app/services/startup_checker.py` | 289 | `drafts/legacy/ops/` | 简化为 5 行 init |
| `app/services/snapshot_service.py` | 216 | `drafts/legacy/snapshot/` | 简化为 VACUUM INTO |
| `app/services/idle_scheduler.py` | 93 | `drafts/legacy/scheduler/` | 简化并入 main |

对应数据模型同步归档，迁移完成后请把本文件状态改为 `extracted`。

## OpenHands 任务格式建议

```
任务：迁出 services/utopia_service.py
1. cp app/services/utopia_service.py → MBclaw-Memory/drafts/legacy/utopia/
2. 从 app/main.py 移除 utopia router 注册
3. rm app/services/utopia_service.py app/routers/utopia.py app/models/utopia.py
4. 删除 tests 中所有 utopia 相关用例
5. pytest 必须仍然通过
6. 提交 PR：chore: extract utopia subsystem to Memory archive
```
