---
type: rejected
status: archived
decided_by: Claude (CTO audit)
verdict: 永久移出 Core
date: 2026-06-21
---

# Thought Collision（思维碰撞引擎）— 永久移出 Core

## 原设计核心要点（保留备查）

- 文件：`MBclaw-Lite/app/services/collision_engine.py`（272 行）
- 思路：随机抽取 2-4 个 successful_memories / praised_skills / proven_approaches，
  组合喂给 LLM 求"创新综合"。
- 数据模型：`ThoughtCollision`。

## 否决理由

1. **不是记忆系统的基础能力**——属于创意产品方向。
2. MVP 阶段没有"足够多的成功经验"供组合，输入空集时退化为噪声。
3. 输出"创意"无评估标准，无回路。
4. 触发条件不清，加大不可预测性，对 OpenHands 难以建立稳定预期。

## 不否决"启发"

如果未来要做创意类产品，可以重启，但**不属于"长期记忆"项目范畴**。

## 关联

- 替代/对照：无（这是独立特性）
- 上游决策：[[2026-06-21_mvp-v2-scope]]
