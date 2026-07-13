# 健康检查

## 运行中服务
- `8000`：mother-server.main:app
- `8100`：控制面板后端
- `3000`：OpenHands 服务
- `8002`：OpenHands agent server
- `904`：qqbot_bridge.py

## 关注项
- qqbot 是否真正回消息。
- 母体网关是否可稳定处理 chat 请求。
- TokenPool / 母体 / 控制面板之间的边界。
