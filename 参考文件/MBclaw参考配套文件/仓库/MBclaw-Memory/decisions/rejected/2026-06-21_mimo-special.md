---
type: rejected
status: archived
decided_by: Claude (CTO survival review)
verdict: 降级为普通 provider
date: 2026-06-21
---

# MiMo Code 特殊化适配 — 降级为普通 provider

## 原设计核心
- 文件：`llm/mimo_adapter.py` (194 行) + 配置页面特殊位
- 思路：MiMo 作为一等公民，独立适配 + 免费试用流程 + 配置页特殊位

## 否决理由
1. **单一 provider 特殊地位 = 战略锁死**
2. MBclaw 应 provider-agnostic，统一 OpenAI 兼容协议
3. "免费试用"为 MiMo 写专用逻辑 → 商业耦合
4. 大部分 provider（含 MiMo）已支持 OpenAI 兼容，无需独立适配

## 处置
- R0：删除 `mimo_adapter.py` 特殊路径
- MiMo 改走 `llm_client` 统一入口，配置形式与其他 provider 一致：`{name, base_url, api_key, model}`
- 试用流程移出 Core，归 Design `design/llm/free-trial-tracking.md`（不实施）

## 关联
- 架构：`design/architecture/ARCH-r0.md` §7
- 上游：[[2026-06-21_mvp-v2-scope]]
