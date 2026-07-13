# MiClaw 劫持方案 — 保留工具，替换内核

## 目标
保留MiClaw全部91个工具 + MCP协议 + 语音唤醒(AIVSE SDK)，把AI内核换成OpenClaw/爱玛仕。

## 核心发现

### 调用链
```
用户输入 → Agent调度 → Taiyi SDK → ILLMManager IPC → LLMManagerService → HTTP API
                                                                                    ↓
                                                                    https://api.mify.mioffice.cn/v1/chat/completions
                                                                                    ↓
                                                                              OpenAI兼容格式
```

### 关键类
- `com.xiaomi.taiyi.sdk.llm.ipc.ILLMManager` — LLM管理器IPC接口
- `com.xiaomi.taiyi.sdk.llm.ipc.ILLMService` — LLM服务IPC接口
- `com.xiaomi.taiyi.sdk.llm.ipc.ILLMClient` — LLM客户端IPC接口
- `com.xiaomi.taiyi.sdk.llm.data.LLMTask` — LLM任务数据类
- `com.xiaomi.aiservice.llmmanager.LLMManagerService` — LLM管理服务
- `com.xiaomi.taiyi.sdk.common.AIKeys` — API密钥配置

### 数据格式
- Taiyi SDK使用AIFrame/AIRequest/AIResponse进行数据传输
- 支持JSON和protobuf格式
- API端点是OpenAI兼容的`/v1/chat/completions`

## 三种劫持方案

### 方案A：Hosts劫持 + 本地代理（最简单，推荐）

**原理：** 修改手机hosts文件，把`api.mify.mioffice.cn`指向本地，本地代理转发到OpenClaw。

**步骤：**
1. 修改`/system/etc/hosts`，添加：
   ```
   127.0.0.1 api.mify.mioffice.cn
   ```

2. 在手机上启动本地代理（Python/Node.js），监听443端口：
   - 接收MiClaw的OpenAI格式请求
   - 转发到OpenClaw Gateway（端口18789或19001）
   - 返回OpenAI格式响应

3. 代理需要处理HTTPS：
   - 生成自签名CA证书
   - 安装到系统信任证书存储
   - 代理做MITM解密

**优点：** 不需要修改APK，不需要重打包
**缺点：** 需要处理HTTPS证书问题

### 方案B：APK反编译修改API端点（最彻底）

**原理：** 直接修改APK中的API端点地址。

**步骤：**
1. 用apktool反编译APK
2. 在`classes3.dex`中找到`api.mify.mioffice.cn`
3. 替换为你的服务器地址（如`127.0.0.1:18789`或ECS地址）
4. 重打包APK
5. 用核心破解跳过签名验证安装

**优点：** 最彻底，完全控制
**缺点：** 需要反编译工具，重打包可能有兼容性问题

### 方案C：MCP Server注入（最灵活）

**原理：** MiClaw支持个人MCP Server注册，通过MCP协议拦截所有调用。

**步骤：**
1. 编写自定义MCP Server
2. 注册到MiClaw的MCP配置
3. MCP Server拦截所有tool调用
4. 把LLM调用转发到OpenClaw/Hermes

**优点：** 不修改MiClaw，完全合法
**缺点：** 只能拦截tool调用，不能拦截Agent调度

## 推荐方案：A + B 组合

### 阶段1：快速验证（方案A）
1. 在手机上设置hosts劫持
2. 起本地代理转发到OpenClaw
3. 验证MiClaw能否正常工作
4. 测试所有工具是否可用

### 阶段2：彻底改造（方案B）
1. 反编译魔改版APK
2. 修改API端点
3. 优化Agent prompt（可选）
4. 重打包安装

## 实施细节

### 本地代理代码（Python）

```python
#!/usr/bin/env python3
"""
MiClaw LLM代理 - 把OpenAI格式请求转发到OpenClaw
"""
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenClaw Gateway地址
OPENCLAW_URL = "http://127.0.0.1:18789/v1/chat/completions"

@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    # 接收MiClaw的请求
    data = request.json
    
    # 转发到OpenClaw
    # 需要适配OpenClaw的格式
    response = requests.post(OPENCLAW_URL, json=data)
    
    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, ssl_context="adhoc")
```

### Hosts修改脚本

```bash
#!/system/bin/sh
# 需要root权限
mount -o remount,rw /system
echo "127.0.0.1 api.mify.mioffice.cn" >> /system/etc/hosts
mount -o remount,ro /system
```

### 证书安装（用于HTTPS代理）

```bash
# 生成CA证书
openssl req -x509 -newkey rsa:4096 -keyout ca.key -out ca.crt -days 3650 -nodes -subj "/CN=MiClaw Proxy CA"

# 安装到系统信任存储
cp ca.crt /system/etc/security/cacerts/
```

## 需要注意的问题

1. **HTTPS证书问题：** MiClaw使用HTTPS，需要安装自签名CA证书到系统信任存储
2. **Agent调度：** 如果用方案A，Agent调度逻辑还在MiClaw内部，只是LLM调用被转发
3. **工具执行：** 工具执行在MiClaw内部，不受劫持影响
4. **语音唤醒：** AIVSE SDK不受影响，语音唤醒仍然工作
5. **MCP协议：** MCP Server连接不受影响

## 测试计划

1. **基础测试：** 验证MiClaw能否启动，不闪退
2. **LLM测试：** 发送简单消息，验证代理是否收到请求
3. **工具测试：** 测试几个关键工具（天气、闹钟、文件操作）
4. **Agent测试：** 测试子Agent调度是否正常
5. **语音测试：** 测试语音唤醒是否工作

## 文件清单

- `/root/miclaw-apk-analysis/HIJACK_PLAN.md` — 本方案
- `/root/miclaw-apk-analysis/unzip_魔改版带sese/` — 解包的魔改版APK
- `/root/miclaw-apk-analysis/unzip_云端沙箱/` — 解包的云端沙箱版APK

## 下一步

等老板醒了确认后开始实施。主要工作：
1. 在手机上设置hosts劫持
2. 编写本地代理
3. 测试基本功能
4. 根据测试结果调整
