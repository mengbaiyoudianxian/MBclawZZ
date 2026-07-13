# 混合深度思考引擎 v4.0

## 概述

DeepSeek(免费)做大脑生成思考，MiClaw(免费)做手脚执行指令。两者配合实现深度分析，全程免费。

## 架构

```
用户问题
    ↓
MiClaw子Agent (循环控制器)
    ↓
① DeepSeek(8899) → 生成思考+指令
    ↓
② MiClaw解析 → 执行指令 → 真实结果
    ↓
③ 结果喂回DeepSeek → 继续思考
    ↓
④ 循环直到[DONE]
    ↓
⑤ announce回主会话
```

## 使用方法

### Python API
```python
from deepseek_brain import HybridEngine

engine = HybridEngine()
result = engine.run("分析这个文件的内容...")
print(result)
```

### 命令行
```bash
python3 deepseek_brain.py "分析 /path/to/file"
```

### OpenClaw子Agent
```
sessions_spawn(
  task="用混合引擎分析...",
  model="miclaw/xiaomi/mimo-pro",
  taskName="hybrid-analysis"
)
```

## 可用工具

| 指令 | 说明 | 示例 |
|------|------|------|
| `#exec` | 执行shell命令 | `#exec ls -la` |
| `#read` | 读取文件 | `#read /etc/hostname` |
| `#write` | 写入文件 | `#write /tmp/test.txt 内容` |
| `#search` | 联网搜索 | `#search Python教程` |
| `#memory_get` | 读取记忆 | `#memory_get /root/.openclaw/workspace/main/MEMORY.md` |
| `#memory_save` | 保存记忆 | `#memory_save 学到了xxx` |

## DeepSeek输出格式

```
[思考] 我需要分析这个文件...
#exec cat /path/to/file
[等待结果]
[RESULT]文件内容...[/RESULT]
[思考] 文件内容显示...
分析结果是...
[DONE]
```

## 配置

环境变量：
- `DEEPSEEK_API` — DeepSeek API地址 (默认: http://localhost:8899)
- `DEEPSEEK_MODEL` — DeepSeek模型 (默认: deepseek-flash)

## 测试

```bash
python3 test_suite.py           # 基础测试
python3 test_suite.py --with-api  # 包含API测试
```

## 注意事项

1. DeepSeek代理(8899)返回流式响应，需要特殊处理
2. conversation_id会自动保存和恢复
3. 超过1小时未对话会自动刷新记忆
4. 最大循环轮数默认20轮，可在代码中修改
