# GitHub 仓库清单

这份清单记录当前账号 `mengbaiyoudianxian` 下已确认的仓库、用途、与 MBclaw 的关系，以及当前优先级。

## P0 — 主线与基础设施

| 仓库 | 作用 | 与 MBclaw 关系 | 当前判断 |
|---|---|---|---|
| `mbclaw-mother` | MBclaw 母体主线，包含 Gateway、Memory、Runtime、Planner、Scheduler、sub2api 接入、控制面板 | 主线核心 | 最优先研究与接手 |
| `MBclawZZ` | 当前总工作区 | 接手工作区 | 作为总目录与施工地基 |
| `MBclaw-Server` | 旧/并行后端总仓 | 历史与参考 | 需要对照主线后再判断 |
| `MBclaw-Android` | Android 客户端 | 客户端参考 | 需要对照 APK 端整理 |
| `MBclaw-Memory` | 历史经验库与方案沉淀 | 记忆参考 | 适合放入参考配套文件 |
| `MBclaw-workspace` | 旧工作区聚合仓 | 工作区参考 | 适合作为历史对照 |
| `MBclaw` | 早期总体设计仓 | 总体设计参考 | 适合作为理念来源 |
| `7.03kai` | 归档与混合材料仓 | 归档/历史参考 | 需判断是否保留价值 |

## P1 — 关键能力参考

| 仓库 | 作用 | 与 MBclaw 关系 | 当前判断 |
|---|---|---|---|
| `OpenClaw` | 平台化、插件、Skills、Agent 编排 | 架构天花板参考 | 值得重点借鉴，不直接照搬 |
| `OpenHands` | Agent runtime、工具执行、SDK 分层 | 执行型运行时参考 | 重点借鉴 runtime 分层 |
| `LiteLLM` | 模型网关、fallback、兼容层、路由 | sub2api/模型入口参考 | 重点借鉴路由与冷却思路 |
| `mem0` | 长期记忆与记忆 API | 记忆系统参考 | 借鉴语义与接口形状 |
| `GraphRAG` | 图谱化知识组织 | 长期知识结构参考 | 远期参考 |
| `modelcontextprotocol` | MCP 协议与 SDK | 工具协议参考 | 适合做接口对齐 |
| `agentskills` | Skills 组织与说明方式 | 技能系统参考 | 适合做工具索引设计 |
| `Claude-Code` | 终端编码代理 | 工作流参考 | 借鉴任务推进与命令执行 |
| `Codex-CLI` | 终端编码代理 | 工作流参考 | 借鉴 runtime/任务流 |
| `FreeLLMAPI` | 兼容网关/中转思路 | sub2api 旁路参考 | 仅保留可复用点 |
| `miclaw_api_bridge` | MiClaw/API 桥接 | APK/桥接参考 | 仅保留桥接思想 |

## P2 — 历史沉淀与归档候选

| 仓库 | 作用 | 与 MBclaw 关系 | 当前判断 |
|---|---|---|---|
| `mbclaw-jindu-xiangjie` | 进度追踪与日志沉淀 | 进度参考 | 可归并到总览端 |
| `work-transfer` | 文件互转/交接 | 交接参考 | 可并入交接工作区 |
| `MBclaw-Lite` | 轻量实验 | 历史实验 | 视内容决定保留或归档 |
| `miclaw-apk-analysis` | APK 逆向分析 | 技术参考 | 仅保留分析结论 |
| `freellmapi` | 兼容 API 的早期参考 | sub2api 历史参考 | 仅保留有用文档 |

## 结论

1. **当前最新主线仓库是 `mbclaw-mother`**。
2. **`MBclawZZ` 是当前接手与整理的总工作区**。
3. **OpenClaw、OpenHands、LiteLLM、mem0、MCP 是高价值参考，不是直接照搬目标**。
4. **历史仓库不应直接混入主线，先放参考或归档，再做二次判断**。
5. **后续施工优先级：主线边界 → sub2api 整理 → 交接摘要 → 归档清理**。
