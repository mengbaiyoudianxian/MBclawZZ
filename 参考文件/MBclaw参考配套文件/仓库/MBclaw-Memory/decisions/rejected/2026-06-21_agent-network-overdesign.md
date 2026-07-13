---
type: rejected
status: archived
decided_by: Claude (CTO agent review, self-corrected)
verdict: 禁止 6 个 Agent 反模式；不禁止未来功能型 Agent
date: 2026-06-21
note: 标题与措辞已自我修正（见 logs/2026-06-21_cto-self-correction.md）
---

# 6 个 Agent 反模式 — 永久禁止（不是禁止 Agent 本身）

## 上下文

Lite 现状：39 services 中 7 个直接服务于"虚构的多 Agent"假设（agent_runtime / sub_agent_coordinator / dual_key / auto_mode / approval_gate 多维 / task_queue / skill_extractor）。
R0 审计判定为过度设计，移出 Core。

## 真正永久禁止的 6 条

| # | 反模式 | 禁止理由 |
|---|---|---|
| 1 | 内部 Agent 互调形成循环（A→B→A） | 状态机爆炸，无法调试 |
| 2 | 同模型 Dual-Key 互评 | 系统性偏见无证据收益 |
| 3 | MBclaw 进程内同时跑多个 Agent | 违反单进程限制 |
| 4 | 提前为"未来扩展"造 Agent 框架 | 已犯过（438 行 agent_runtime） |
| 5 | 无安全边界的 Auto Mode | 工程伦理 |
| 6 | Agent 持自己的存储绕过 MemoryRepo | 一致性灾难 |

## 明确**不**禁止的

- ✅ R2/R3+ 演化为功能型 Agent 系统
- ✅ R2 引入 ReflectionAgent（单步、3 工具）
- ✅ 多个外部 Agent 通过 HTTP 调 MBclaw（这就是预期形态）
- ✅ 在 6 反模式之外的任何新 Agent 设计

## 替代/允许的形态

R0/R1：MBclaw 无内部 Agent，外部 Agent 通过 HTTP 调用：
```
OpenHands / Claude Code / 自写 App
        │ HTTP REST
        ▼
   MBclaw（纯记忆服务）
```

R3+ 即使 MBclaw 内部出现功能型 Agent，多 Agent 协作仍**只能通过 HTTP**：
```
Agent A (外部进程) ──┐
                    ├──▶ MBclaw HTTP API ──▶ SQLite
Agent B (外部进程) ──┘
```

## 教训

> "多 Agent 协作"是 2024-2025 年最被高估的架构模式。
> 多数任务用单 Agent + 好的工具就能完成。
> 但**禁止反模式 ≠ 禁止演化**——把"防止再犯"伪装成"永远不做"是另一种不诚实。
> CTO 也会用力过猛，必须自我修正并留痕。

## 关联

- 设计：[[architecture/ARCH-r0]] §6 / MBclaw `design/agent/AGENT-r0.md`
- 自我修正记录：[[logs/2026-06-21_cto-self-correction]]
- 同类否决（仍有效）：[[2026-06-21_dual-key-and-subagent]] [[2026-06-21_auto-mode]] [[2026-06-21_collision-engine]]
