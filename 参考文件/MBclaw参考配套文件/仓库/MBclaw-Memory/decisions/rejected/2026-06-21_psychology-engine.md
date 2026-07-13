---
type: rejected
status: archived
decided_by: Claude (CTO audit)
verdict: 永久移出 Core
date: 2026-06-21
---

# Psychology Engine（用户心理画像）— 永久移出 Core

## 原设计核心要点

- 文件：`psychology_engine.py` (333 行)
- 思路：从用户反馈文本抽情绪词，加权打分映射到 `social_energy/communication/structure_pref/decision_style`。
- 数据模型：`UserProfile / PositivePattern`。

## 否决理由

1. **伪科学评分**——情绪词→维度的权重表（如"温暖" +0.10 social_energy）**无任何心理学依据**。
2. 单语种、单词典覆盖不充分；中英混合即崩。
3. 评分用途未定义，下游消费者不存在。
4. 隐含 PII 风险——存储用户心理画像应有合规审计，MVP 不具备。

## 教训

> 看上去"很 AI"的特性，最危险——容易在评审中被默认接受。
> 必须问"评分给谁用？信号怎么验证？错了谁负责？"

## 关联

- 同类：[[2026-06-21_utopia-plan]] [[2026-06-21_collision-engine]]
- 上游：[[2026-06-21_mvp-v2-scope]]
