# Legacy Services Archive

R0 阶段从 MBclaw-Lite main 分支物理迁出的旧代码。
文件内容未修改，仅供 R2+ 重启时参考。

## 迁出清单

| 文件 | 源路径 | 分类 | 处置 |
|------|--------|------|------|
| utopia_service.py | app/services/ | utopia | 永久移出 |
| chat_extractor.py | app/services/ | utopia | 永久移出 |
| psychology_engine.py | app/services/ | psychology | 永久移出 |
| collision_engine.py | app/services/ | collision | 永久移出 |
| sub_agent_coordinator.py | app/services/ | agent | 永久移出 |
| dual_key.py | app/services/ | agent | 永久移出 |
| agent_runtime.py | app/services/ | agent | R2 重写参考 |
| skill_extractor.py | app/services/ | agent | R2 重写参考 |
| curator.py | app/services/ | agent | R2 重写参考 |
| auto_mode.py | app/services/ | agent | R2 重写参考 |
| feedback_service.py | app/services/ | feedback | R2 重写参考 |
| classification_service.py | app/services/ | classification | R2 重写参考 |
| vector_store.py | app/services/ | vector | R2 重写参考 |
| layered_search.py | app/services/ | search | 合并入新 search |
| integration_service.py | app/services/ | integrations | R3 重启参考 |
| i18n_service.py | app/services/ | i18n | R3 重启参考 |
| approval_gate.py | app/services/ | approval | 简化版进 R1 |
| task_queue.py | app/services/ | queue | R2 重启参考 |
| message_priority.py | app/services/ | queue | R2 重启参考 |
| tool_service.py | app/services/ | tools | R2 重启参考 |
| model_service.py | app/services/ | llm | R2 重启参考 |
| startup_checker.py | app/services/ | ops | 简化为 5 行 init |
| snapshot_service.py | app/services/ | snapshot | 简化为 VACUUM INTO |
| idle_scheduler.py | app/services/ | scheduler | 简化并入 main |

同步归档对应 routers/ 和 models/ 文件。
源 commit: `d4ea0d26417d5fb2fee0e81c74c331f346221e1b`
迁出日期: 2026-06-21
操作方: OpenHands (M1)
