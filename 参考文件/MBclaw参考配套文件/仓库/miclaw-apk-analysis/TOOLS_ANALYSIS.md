# MiClaw工具系统分析

## 工具总数统计

### 魔改版带sese (最完整)
- **tool_overlays.json**: 386个工具覆盖
- **tools_catalog.json**: 18个系统工具定义
- **agents**: 26个Agent

### 有本地沙箱版
- **tool_groups.json**: 92个工具模式
- **sandbox_mcp_server.py**: 7个沙箱工具
- **agents**: 13个Agent

### 云端沙箱版
- **enterprise_mcp_servers.json**: 云端MCP配置
- **agents**: 11个Agent

### 可以安装但闪退版
- **sandbox_mcp_server.py**: 7个沙箱工具
- **sub_agents_config.json**: 子Agent配置
- **agents**: 2个Agent (精简版)

## 工具分类

### 系统设备 (42个工具)
- WiFi管理: list_wifi_networks, connect_wifi, disconnect_wifi, switch_wifi, wifi_info
- 蓝牙管理: bluetooth_scan, bluetooth_connect, bluetooth_disconnect, bluetooth_paired_devices, bluetooth_status, bluetooth_toggle
- 剪贴板: clipboard
- 扫码: scanner__*
- 设置: settings__*, misettings__*
- 壁纸: manage_wallpaper
- 安全: securitycenter__*

### 通讯 (30个工具)
- 短信: send_sms, read_sms, manage_sms_event
- 电话: dial_phone, hang_up, call_log_list, call_log_delete, manage_call_event, reply_to_caller
- 联系人: search_contacts, manage_contacts
- 通话记录: call_log_list, call_log_delete

### 文件 (13个工具)
- 读写: read_file, write_file, edit_file, append_file
- 操作: copy_file, move_file, delete_file, search_files, list_files
- 搜索: file_grep
- 目录: create_directory, list_directory

### 媒体 (42个工具)
- 相机: camera
- 录屏: screenrecorder__*
- 录音: soundrecorder__*
- 媒体库: media_store, list_media_images
- 图库: gallery__*
- 媒体编辑: mediaeditor__*
- 控制: control_media, get_media_info

### 应用 (11个工具)
- 管理: app_manager, app_shortcut
- 使用: app_usage
- 商店: xiaomi_appstore__app_search, xiaomi_appstore__app_download

### 日历日程 (17个工具)
- 创建: create_calendar_event
- 读取: read_calendar
- 更新: update_calendar_event
- 删除: delete_calendar_event
- 日程: calendar__*

### 笔记 (27个工具)
- 笔记: notes__*

### 浏览器 (9个工具)
- 浏览器: browser_open, browser_click, browser_input, browser_extract, browser_login, browser_close

### 语音管理 (7个工具)
- TTS: tts_set_voice, tts_list_voices
- 语音: set_tts_enabled

### 多设备互联 (9个工具)
- 设备: device_list, device_coord, device_messages, device_send_image
- 任务: send_task_to_device, broadcast_query

### 管理 (12个工具)
- 提醒: create_reminder, update_reminder, delete_reminder, query_reminders
- 闹钟: deskclock__deskclock_add_alarm, deskclock__deskclock_query_alarms, deskclock__deskclock_update_alarm, deskclock__deskclock_delete_alarm
- 定时器: timer

### 搜索 (3个工具)
- 搜索: web_search, url_fetch

### 生活服务 (63个工具)
- 地图: amap__*, baidumap__*
- 出行: caocao__*, hellobike__*, tongcheng__*, ctrip_flight__*, ctrip_hotel__*, ctrip_train__*, tripnow__*, t3go__*
- 购物: jingdong__*, xianyu__*
- 音乐: kugou-music__*
- 知乎: zhihu__*

### 图片编辑 (26个工具)
- 图片: image_process, image_editor__*

### 账号 (21个工具)
- 账号: account__*

### Agent (13个工具)
- Agent管理: create_agent, update_agent, delete_agent, list_agents, search_agents, start_agent
- 子Agent: agent_osbot_calendar, agent_osbot_content_assistant, agent_osbot_imaging_assistant, agent_osbot_communication_assistant, agent_osbot_xiaomihome, agent_osbot_os_helper, agent_osbot_entertainment_assistant, agent_osbot_account_cloud, agent_osbot_device_interconnect, agent_osbot_worker

### 云服务 (8个工具)
- 云服务: cloudservice__*

### 开发者 (22个工具)
- 终端: terminal__*
- 测试: testproducer__*, testconsumer__*

## 沙箱工具 (sandbox_mcp_server.py)

1. **shell_exec** - 执行shell命令
2. **code_run** - 执行Python/JavaScript/Shell代码
3. **pip_install** - 安装Python包
4. **npm_install** - 安装Node.js包
5. **data_analysis** - 数据分析 (pandas)
6. **image_process** - 图片处理 (Pillow)
7. **file_convert** - 文件转换 (pandoc/ffmpeg)

## MCP协议

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

## 工具安全级别

根据tool_overlays.json中的配置：
- **无限制**: 日历读写、闹钟、录屏、录音、笔记、天气、地图、终端
- **需确认**: 通讯录修改、短信发送、通话管理
- **禁止**: 未列出的敏感操作

## 劫持策略

### 保留的工具
- 所有系统工具 (WiFi、蓝牙、设置等)
- 所有文件操作工具
- 所有媒体工具
- 所有通讯工具
- 所有Agent工具
- 所有MCP工具

### 可能需要修改的工具
- web_search (可能需要替换搜索源)
- url_fetch (可能需要代理)

### 不受影响的工具
- 语音唤醒 (AIVSE SDK)
- 本地沙箱 (sandbox_mcp_server.py)
- MCP协议
