# MBclaw Server

MBclaw 后端服务 — FastAPI + SQLite，包含管理面板、MiClaw 桥接、母体运行时、Token 池、文件上传、下载统计。

## 结构

```
main.py              # 服务入口
router.py            # 管理面板路由 (30+ API)
bridge_manager.py    # MiClaw 桥接管理
server_app/
  admin/             # 管理面板后端 (HTML/JS/Python)
  mother/            # 母体运行时模块
  api.py             # MBclaw Lite 核心 API
  agent.py           # Agent 引擎
  tools.py           # 工具注册
  ...
```

## 部署

```bash
APP_DIR=/opt/mbclaw bash deploy_unified_mother.sh
```

## API 端点

详见 `API_CATALOG.md`
