# MiClaw劫持项目

## 目标
保留MiClaw全部工具能力，把AI内核换成OpenClaw/爱玛仕。

## 文件结构

```
miclaw-apk-analysis/
├── HIJACK_PLAN.md          # 劫持方案详细文档
├── TOOLS_ANALYSIS.md       # 工具系统分析
├── README.md               # 本文件
├── proxy/                  # 代理代码
│   ├── miclaw_proxy.py     # LLM代理脚本
│   └── setup.sh            # 手机端设置脚本
├── unzip_云端沙箱/         # 云端沙箱版APK解包
├── unzip_可以安装但是闪退/ # 可以安装但闪退版APK解包
├── unzip_有本地沙箱但安装不了/ # 有本地沙箱版APK解包
└── unzip_魔改版带sese/     # 魔改版APK解包
```

## 快速开始

### 1. 在手机上设置代理

```bash
# 下载代理文件到手机
adb push proxy/ /sdcard/miclaw-proxy/

# 在手机上运行设置脚本
su
cd /sdcard/miclaw-proxy
bash setup.sh
```

### 2. 启动代理

```bash
# 启动代理
/data/adb/miclaw-proxy/start.sh

# 查看日志
tail -f /data/adb/miclaw-proxy/proxy.log
```

### 3. 测试代理

```bash
# 测试代理
/data/adb/miclaw-proxy/test.sh
```

### 4. 重启MiClaw

```bash
# 杀掉MiClaw进程，让它重启
pkill -f com.xiaomi.type
```

## 代理工作原理

```
用户输入 → MiClaw → Taiyi SDK → LLMManagerService
                                      ↓
                              api.mify.mioffice.cn
                                      ↓
                              hosts劫持到127.0.0.1
                                      ↓
                              miclaw_proxy.py (端口8443)
                                      ↓
                              转发到OpenClaw (端口18789)
                                      ↓
                              返回响应给MiClaw
```

## 工具系统

MiClaw有386个工具覆盖，分为以下类别：

- **系统设备**: WiFi、蓝牙、设置、剪贴板 (42个)
- **通讯**: 短信、电话、联系人 (30个)
- **文件**: 读写、操作、搜索 (13个)
- **媒体**: 相机、录屏、录音、图库 (42个)
- **应用**: 管理、商店 (11个)
- **日历日程**: 创建、读取、更新、删除 (17个)
- **笔记**: 笔记管理 (27个)
- **浏览器**: 自动化 (9个)
- **语音管理**: TTS (7个)
- **多设备互联**: 跨设备协作 (9个)
- **管理**: 提醒、闹钟、定时器 (12个)
- **搜索**: 网页搜索 (3个)
- **生活服务**: 地图、出行、购物、音乐 (63个)
- **图片编辑**: 图片处理 (26个)
- **账号**: 账号管理 (21个)
- **Agent**: Agent管理 (13个)
- **云服务**: 云服务 (8个)
- **开发者**: 终端、测试 (22个)

## 沙箱工具

sandbox_mcp_server.py提供7个沙箱工具：

1. **shell_exec** - 执行shell命令
2. **code_run** - 执行Python/JavaScript/Shell代码
3. **pip_install** - 安装Python包
4. **npm_install** - 安装Node.js包
5. **data_analysis** - 数据分析 (pandas)
6. **image_process** - 图片处理 (Pillow)
7. **file_convert** - 文件转换 (pandoc/ffmpeg)

## Agent系统

### 魔改版 (26个Agent)
- osbot.main - 主助手
- osbot.chat - 聊天
- osbot.calendar - 日历
- osbot.call_agent - 电话
- osbot.communication_assistant - 通讯助手
- osbot.content_assistant - 内容助手
- osbot.device_interconnect - 设备互联
- osbot.entertainment_assistant - 娱乐助手
- osbot.feedback - 反馈
- osbot.imaging_assistant - 影像助手
- osbot.nsfw - NSFW内容
- osbot.os_helper - 系统助手
- osbot.overlayassistant - 悬浮助手
- osbot.qiushi - 求是
- osbot.trump - 特朗普
- osbot.web_explore - 网页探索
- osbot.worker - 工作
- osbot.xiaomihome - 小米智能家居
- osbot.zhangxuefeng - 张雪峰
- osbot.account_cloud - 账号云
- osbot.os_helper - 系统助手
- osbot.worker - 工作
- com.android.camera - 相机
- com.xiaomi.lyrabridge-watch - 手表
- com.xiaomi.type - 输入法

## MCP协议

MiClaw支持MCP (Model Context Protocol) 协议，可以连接外部工具服务。

### 企业MCP服务器
- deskclock (闹钟管理)
- screenrecorder (录屏)
- soundrecorder (录音)
- terminal (终端)
- notes (笔记)
- contacts (通讯录)
- amap/baidumap (地图)
- hellobike/caocao (出行)
- zhihu (知乎)
- xiaomi_appstore (应用商店)

### 个人MCP服务器
- 用户自定义，支持飞书、高德等

## 注意事项

1. **需要root权限** - 修改hosts和安装证书需要root
2. **需要OpenClaw Gateway** - 代理转发到OpenClaw，需要先启动Gateway
3. **HTTPS证书** - 需要安装自签名CA证书到系统信任存储
4. **重启MiClaw** - 修改hosts后需要重启MiClaw使修改生效

## 故障排除

### 代理无法启动
- 检查端口是否被占用: `netstat -tlnp | grep 8443`
- 检查Python依赖: `pip3 list | grep flask`

### MiClaw无法连接
- 检查hosts修改: `cat /system/etc/hosts | grep mify`
- 检查代理日志: `tail -f /data/adb/miclaw-proxy/proxy.log`

### 工具无法使用
- 检查OpenClaw Gateway状态: `curl http://127.0.0.1:18789/health`
- 检查代理健康: `curl http://127.0.0.1:8443/health`

## 下一步

1. 在手机上测试代理
2. 验证所有工具是否正常工作
3. 根据测试结果调整代理逻辑
4. 优化Agent prompt (可选)
