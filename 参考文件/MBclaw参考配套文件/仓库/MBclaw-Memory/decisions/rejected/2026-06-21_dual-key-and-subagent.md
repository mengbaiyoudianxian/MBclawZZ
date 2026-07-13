---
type: rejected
status: archived
decided_by: Claude (CTO audit)
verdict: 永久移出 Core
date: 2026-06-21
---

# Dual-Key 协作 & Sub-Agent Coordinator — 永久移出 Core

## 原设计核心要点

- Dual-Key：Key1 执行 → Key2 评价 → Key1 改 → 循环 1-6 次（`services/dual_key.py` 96 行）
- Sub-Agent Coordinator：多个子对话共享通道、反思去重、冲突协商（`sub_agent_coordinator.py` 131 行）

## 否决理由

1. **当前没有任何 Agent 在 Core 跑**——给虚拟需求设计协作框架。
2. Dual-Key：成本翻倍，**同模型同 prompt 容易系统性偏见**——不一定提升质量。
3. Sub-Agent：共享通道、去重、协商三个机制全部基于"已有多个 agent"的前提，假设不成立。
4. 复杂度爆炸：错综的状态流转，调试成本极高。

## 重启条件

- R2 阶段 Agent Runtime 上线且**实测发现单 agent 质量瓶颈**时再评估。
- 评估必须有 A/B：单 agent vs dual/multi，按真实任务集衡量。

## 关联

- 上游：[[2026-06-21_mvp-v2-scope]]
- 相关：[[2026-06-21_agent-runtime-deferred]]
