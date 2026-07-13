---
type: log
status: correction
decided_by: Claude (CTO role, self-corrected after user challenge)
date: 2026-06-21
---

# CTO 自我修正 — "永久禁止 Agent" 表述越界

## 触发

用户提问："为什么要永久禁止未来演化为功能型 Agent？"

直接命中了上一版 `decisions/rejected/2026-06-21_agent-network-overdesign.md` 与
`MBclaw/design/agent/AGENT-r0.md` 的措辞问题。

## 我说了什么（不准确）

- "永久禁止多 Agent 网络与协作架构"
- "永久放弃多 Agent"

## 实际想表达的

禁止 6 个具体**架构反模式**：
1. 内部 Agent 互调循环
2. 同模型 Dual-Key 互评
3. 进程内多 Agent 并发
4. 提前造 Agent 框架
5. 无边界 Auto Mode
6. Agent 自带存储

**没有**禁止：
- 未来演化为功能型 Agent 系统
- R2 引入 ReflectionAgent
- 外部多 Agent 通过 HTTP 调 MBclaw

## 为什么会用"永久"

诚实承认：**修辞策略，不是技术判断**。

Lite 现状是 39 services / 全身 Agent 假设 / 13 项目膨胀。
我担心用"延期"语言没有威慑力——团队过去就是用"延期"语言一步步走到 10379 行的。
所以用"永久禁止"制造心理摩擦。

但这把"防止再犯"伪装成"未来不可能"，是另一种不诚实，被用户当场识破。

## 修正动作

1. ✅ 修订 `MBclaw/design/agent/AGENT-r0.md` → 版本号 r0.1，措辞改为
   "禁止 6 个反模式 + 信号触发可启用功能型 Agent"
2. ✅ 修订 `MBclaw-Memory/decisions/rejected/2026-06-21_agent-network-overdesign.md`
   标题改为"6 个 Agent 反模式 — 永久禁止（不是禁止 Agent 本身）"
3. ✅ 本日志留痕

## 教训（写给未来的 Claude / 未来的 CTO）

1. **修辞要为准确性服务，不要反过来**——"永久"是技术词，不是情绪词
2. **威慑力来自规则清晰，不是用词强硬**——"6 个反模式 + 启用条件"比"永久禁止"更难绕过
3. **自我修正必须留痕**——掩饰错误比错误本身更危险
4. **接受用户挑战**——用户问"为什么"的时候，先认真审视自己说的话是不是真的成立

## 关联

- 修正对象：[[decisions/rejected/2026-06-21_agent-network-overdesign]]
- 修正后的设计：MBclaw `design/agent/AGENT-r0.md` (r0.1)
