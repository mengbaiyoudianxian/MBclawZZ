---
type: rejected
status: archived
decided_by: Claude (CTO audit)
verdict: 永久移出 Core
date: 2026-06-21
---

# 乌托邦计划（Utopia）— 永久移出 Core

## 原设计核心要点

- 文件：`utopia_service.py` (382 行) + `chat_extractor.py` (387 行) + `psychology_engine.py` (333 行)
- 数据模型：`ChatImport / UtopiaInsight / UtopiaTask / UtopiaSubmission` 4 张表
- 流程：
  1. 导入用户聊天记录
  2. 去 PII + 分类（bug/praise/complaint/feature_request/skill_wish）
  3. 抽取洞察并打分
  4. 生成任务队列
  5. 用户×0.80 + 自评×0.20 评判提交

## 否决理由

1. **完全偏离"长期记忆"使命**——这是"产品想法采集系统"。
2. PII 处理仅做 5 类正则，**风险高**而强度不够，单独立项才合规。
3. "0.80/0.20"评分系数无依据，伪精确。
4. 数据闭环不存在——抽取后没人消费。

## 教训

> 任何与 MVP 单一目标不直接相关的特性，**不能进 Core**，即便代码已写完。

## 关联

- 类似裁剪：[[2026-06-21_psychology-engine]] [[2026-06-21_collision-engine]]
- 上游：[[2026-06-21_mvp-v2-scope]]
