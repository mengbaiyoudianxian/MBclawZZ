# MBclaw-Memory

> **仓库定位**：MBclaw 项目经验库。
> 存放：被否决方案 / 历史失败 / 灵感草稿 / 实验记录 / Claude 分析 / OpenHands 日志。
> 目的：**不让任何一次失败白费**。

## 目录约定

```
decisions/
  rejected/        # 被否决的设计/技术选型，含原因
experiments/
  failed/          # 失败的实验，含输入/输出/教训
inspirations/      # 创意草稿（未评估）
drafts/            # 未成熟的设计稿
logs/              # Claude 审计 / OpenHands 开发日志
```

## 文件命名

`YYYY-MM-DD_<short-slug>.md` — 永远带日期，便于回溯。

## 写入规则

1. 每条记录必须含 frontmatter：`type` / `status` / `decided_by` / `verdict`。
2. 必须写"为什么"，不能只写"是什么"。
3. 否决项必须留存原始设计的核心要点，**不能只留结论**——否则未来无法复盘。

## 与其他仓库的关系

```
设计提案（MBclaw）
   ├── 通过 → 落地 MBclaw-Lite（Core）
   └── 否决 → 归档 MBclaw-Memory（本仓库）
失败实验（任何来源）
   └── 沉淀 MBclaw-Memory
```

## 当前活跃任务

- **M1**：物理迁出 14 个旧 services（详见 [drafts/2026-06-21_legacy-services-to-be-extracted.md](drafts/2026-06-21_legacy-services-to-be-extracted.md)）
- **M2**：一次性导出 main 分支 SQLite 数据
- **M3**：实施中新失败 / 否决实时归档

执行计划入口：[MBclaw/design/roadmap/DEV-PLAN-r0.md](https://github.com/mengbaiyoudianxian/MBclaw/blob/main/design/roadmap/DEV-PLAN-r0.md)
