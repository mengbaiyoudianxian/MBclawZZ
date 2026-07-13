---
type: failed
status: archived
decided_by: Claude (CTO audit)
verdict: 过早优化，R2 之前回退到 L1
date: 2026-06-21
---

# 实验失败：分层搜索 L1+L2+L3 过早实施

## 实验内容

- `services/layered_search.py` + `services/vector_store.py` + ChromaDB 依赖。
- 三层：L1 jieba 关键词 / L2 TF-IDF / L3 ChromaDB 向量。

## 为什么算"失败"

1. **没有数据支撑**——没有真实查询日志衡量 L1 命中率，就上 L2/L3。
2. ChromaDB 在测试环境持有文件锁（见 `tests/conftest.py` 必须特殊处理）——首个生产风险信号。
3. 三层混合的路由策略没有任何"什么 query 走哪层"的判据。
4. 引入向量库 → 启动检查 / 备份 / 部署都变复杂（StartupChecker 因此膨胀）。

## 教训

> "万一不够用就有"是反模式。先 L1 跑，命中率不足再加 L2/L3，每层都要带证据上车。

## 后续

- R1：搜索退化到 L1（jieba + SQLite FTS5）。
- R2：等真实查询日志，命中率 < 70% 才启用向量。

## 关联

- 上游：[[2026-06-21_mvp-v2-scope]]
- 架构：见 MBclaw `design/architecture/ARCH-v2.md`
