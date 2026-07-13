# M1 执行记录 — 2026-06-21

## 迁出统计
- 源: MBclaw-Lite@d4ea0d2 (main)
- 目标: MBclaw-Memory/drafts/legacy/
- 文件: 47 (24 services + 14 routers + 9 models)
- 分类: 17 个目录
- 未修改任何代码内容

## M2 状态
- 跳过: main 分支 SQLite 数据库未提交到 git (data/mbclaw.db 被 .gitignore 排除)
- 无法导出

## 执行中的修正
1. 循环导入: api.py ↔ main.py → 将 append_transcript 移至 api.py
2. merge() UNIQUE 约束: Summary.session_id → 改为 delete-then-insert
3. LLMClient 空 API key → 提前检测，返回 503 明确错误
4. test_db 隔离: importlib.reload 污染 → 添加 app.models reload

## 备注
- 所有问题在提交前修正，未产生失败归档
- R0 核心代码 730 行，53 测试全绿
