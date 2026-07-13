# MiClaw劫持测试计划

## 测试目标
验证MiClaw在劫持后能否正常工作，所有工具是否可用。

## 测试环境
- 设备: 小米17 Pro Max
- 系统: Android 16, HyperOS 3.0
- Root: KernelSU
- OpenClaw Gateway: 端口18789或19001

## 测试步骤

### 阶段1: 代理基础测试

#### 1.1 代理启动测试
```bash
# 启动代理
/data/adb/miclaw-proxy/start.sh

# 检查代理状态
curl http://127.0.0.1:8443/health

# 期望输出:
# {
#   "status": "ok",
#   "requests": 0,
#   "target": "openclaw",
#   "timestamp": "..."
# }
```

#### 1.2 代理转发测试
```bash
# 测试LLM转发
curl -X POST http://127.0.0.1:8443/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "miclaw-hijacked",
        "messages": [
            {"role": "user", "content": "你好"}
        ]
    }'

# 期望输出: OpenAI格式的响应
```

### 阶段2: MiClaw集成测试

#### 2.1 MiClaw启动测试
```bash
# 杀掉MiClaw进程
pkill -f com.xiaomi.type

# 等待MiClaw重启
sleep 5

# 检查MiClaw是否运行
ps | grep com.xiaomi.type

# 检查代理日志
tail -f /data/adb/miclaw-proxy/proxy.log

# 期望: 看到MiClaw的LLM请求
```

#### 2.2 基本对话测试
```bash
# 在MiClaw中发送消息
# "你好，你是谁？"

# 检查代理日志
tail -f /data/adb/miclaw-proxy/proxy.log

# 期望: 看到请求转发到OpenClaw，收到响应
```

### 阶段3: 工具功能测试

#### 3.1 系统工具测试
```bash
# 测试WiFi工具
# "查看当前WiFi连接"

# 测试蓝牙工具
# "扫描附近蓝牙设备"

# 测试剪贴板工具
# "读取剪贴板内容"

# 期望: 所有系统工具正常工作
```

#### 3.2 文件工具测试
```bash
# 测试文件读取
# "读取/sdcard/Download/test.txt"

# 测试文件写入
# "创建文件/sdcard/Download/test.txt，内容为'hello'"

# 测试文件搜索
# "搜索/sdcard/Download目录下的txt文件"

# 期望: 所有文件工具正常工作
```

#### 3.3 媒体工具测试
```bash
# 测试相机
# "拍照"

# 测试录屏
# "开始录屏"

# 测试媒体库
# "查看最近的照片"

# 期望: 所有媒体工具正常工作
```

#### 3.4 通讯工具测试
```bash
# 测试短信
# "查看最近的短信"

# 测试联系人
# "搜索联系人张三"

# 测试通话记录
# "查看最近的通话记录"

# 期望: 所有通讯工具正常工作
```

#### 3.5 日历工具测试
```bash
# 测试日历
# "查看今天的日程"

# 测试创建日程
# "创建明天下午3点的会议"

# 期望: 所有日历工具正常工作
```

#### 3.6 笔记工具测试
```bash
# 测试笔记
# "查看笔记"

# 测试创建笔记
# "创建笔记'测试笔记'"

# 期望: 所有笔记工具正常工作
```

### 阶段4: Agent调度测试

#### 4.1 子Agent测试
```bash
# 测试日历Agent
# "查看今天的日程安排"

# 测试内容助手
# "搜索最近的新闻"

# 测试智能家居
# "查看智能家居设备"

# 期望: 子Agent正常调度和执行
```

#### 4.2 多Agent协作测试
```bash
# 测试复杂任务
# "帮我安排明天的日程，包括会议和提醒"

# 期望: 多个Agent协作完成任务
```

### 阶段5: 语音唤醒测试

#### 5.1 语音唤醒测试
```bash
# 说"小爱同学"

# 期望: 语音唤醒正常工作
# 注意: 这个测试需要实际语音，无法通过命令行测试
```

### 阶段6: MCP协议测试

#### 6.1 MCP服务器测试
```bash
# 测试MCP工具
# "使用闹钟工具创建闹钟"

# 期望: MCP工具正常工作
```

### 阶段7: 沙箱工具测试

#### 7.1 沙箱工具测试
```bash
# 测试shell_exec
# "执行命令ls -la"

# 测试code_run
# "执行Python代码print('hello')"

# 期望: 沙箱工具正常工作
```

## 测试结果记录

### 测试通过标准
- 所有工具正常工作
- Agent调度正常
- 语音唤醒正常
- MCP协议正常
- 沙箱工具正常

### 测试失败处理
- 检查代理日志
- 检查OpenClaw Gateway状态
- 检查MiClaw日志
- 根据错误信息调整代理逻辑

## 回滚计划

如果劫持失败，可以快速回滚：

```bash
# 1. 恢复hosts文件
mount -o remount,rw /system
sed -i '/api.mify.mioffice.cn/d' /system/etc/hosts
mount -o remount,ro /system

# 2. 停止代理
/data/adb/miclaw-proxy/stop.sh

# 3. 重启MiClaw
pkill -f com.xiaomi.type
```

## 测试时间表

- 阶段1: 代理基础测试 (10分钟)
- 阶段2: MiClaw集成测试 (15分钟)
- 阶段3: 工具功能测试 (30分钟)
- 阶段4: Agent调度测试 (20分钟)
- 阶段5: 语音唤醒测试 (10分钟)
- 阶段6: MCP协议测试 (15分钟)
- 阶段7: 沙箱工具测试 (15分钟)

总计: 约2小时
