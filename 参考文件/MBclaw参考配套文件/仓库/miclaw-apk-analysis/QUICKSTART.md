# MiClaw劫持 - 快速开始指南

## 老板醒了看这里

### 一句话总结
MiClaw用的是OpenAI兼容的API端点 `api.mify.mioffice.cn`，可以hosts劫持到本地代理，代理转发到OpenClaw。所有工具保留，只换AI内核。

### 准备工作
1. 手机已root (KernelSU)
2. OpenClaw Gateway已启动 (端口18789或19001)
3. Python3已安装 (Termux)

### 三步搞定

#### 第一步: 把代理文件推到手机
```bash
# 在电脑上执行
adb push /root/miclaw-apk-analysis/proxy/ /sdcard/miclaw-proxy/
```

#### 第二步: 在手机上运行设置脚本
```bash
# 在手机Termux中执行
su
cd /sdcard/miclaw-proxy
bash setup.sh
```

#### 第三步: 启动代理并测试
```bash
# 启动代理
/data/adb/miclaw-proxy/start.sh

# 测试代理
/data/adb/miclaw-proxy/test.sh

# 重启MiClaw
pkill -f com.xiaomi.type
```

### 验证是否成功
1. 打开MiClaw，发送"你好"
2. 检查代理日志: `tail -f /data/adb/miclaw-proxy/proxy.log`
3. 如果看到请求转发到OpenClaw，说明成功

### 如果出问题
```bash
# 回滚: 恢复hosts
mount -o remount,rw /system
sed -i '/api.mify.mioffice.cn/d' /system/etc/hosts
mount -o remount,ro /system

# 停止代理
/data/adb/miclaw-proxy/stop.sh

# 重启MiClaw
pkill -f com.xiaomi.type
```

### 文件位置
- 代理代码: `/root/miclaw-apk-analysis/proxy/`
- 劫持方案: `/root/miclaw-apk-analysis/HIJACK_PLAN.md`
- 工具分析: `/root/miclaw-apk-analysis/TOOLS_ANALYSIS.md`
- 测试计划: `/root/miclaw-apk-analysis/TEST_PLAN.md`
- APK解包: `/root/miclaw-apk-analysis/unzip_魔改版带sese/`

### 代理工作原理
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

### 工具保留情况
- ✅ 系统工具 (WiFi、蓝牙、设置)
- ✅ 文件工具 (读写、搜索)
- ✅ 媒体工具 (相机、录屏、录音)
- ✅ 通讯工具 (短信、电话、联系人)
- ✅ 日历工具 (日程管理)
- ✅ 笔记工具 (笔记管理)
- ✅ 浏览器工具 (自动化)
- ✅ 语音工具 (TTS)
- ✅ 多设备互联 (跨设备协作)
- ✅ 管理工具 (提醒、闹钟)
- ✅ 搜索工具 (网页搜索)
- ✅ 生活服务 (地图、出行、购物)
- ✅ 图片编辑 (图片处理)
- ✅ 账号工具 (账号管理)
- ✅ Agent工具 (Agent管理)
- ✅ 云服务工具 (云服务)
- ✅ 开发者工具 (终端、测试)
- ✅ MCP协议 (外部工具)
- ✅ 沙箱工具 (代码执行)
- ✅ 语音唤醒 (AIVSE SDK)

### 下一步优化
1. 测试所有工具是否正常工作
2. 根据测试结果调整代理逻辑
3. 优化Agent prompt (可选)
4. 考虑APK反编译修改 (更彻底)
