# GitHub精品参考

## 已拉取参考仓库
- `modelcontextprotocol/`：MCP 规范与文档主仓。
- `python-sdk/`：MCP Python SDK。
- `typescript-sdk/`：MCP TypeScript SDK。
- `java-sdk/`：MCP Java SDK。
- `go-sdk/`：MCP Go SDK。
- `rust-sdk/`：MCP Rust SDK。
- `csharp-sdk/`：MCP C# SDK。
- `swift-sdk/`：MCP Swift SDK。
- `kotlin-sdk/`：MCP Kotlin SDK。
- `ruby-sdk/`：MCP Ruby SDK。
- `php-sdk/`：MCP PHP SDK。
- `mem0/`：Mem0 记忆层参考。
- `GraphRAG/`：GraphRAG 方案参考。
- `LiteLLM/`：统一模型网关 / 路由 / 兼容层参考。
- `OpenHands/`：OpenHands 代理与自动化参考。
- `Codex-CLI/`：终端编码代理参考。
- `Claude-Code/`：Claude Code 终端代理参考。
- `miclaw_api_bridge/`：MiClaw API 桥接参考。
- `OpenClaw/`：OpenClaw 主平台参考。
- `FreeLLMAPI/`：FreeLLMAPI 路由与兼容层参考。
- `agentskills/`：Agent Skills 规范与文档参考。

## 使用原则
1. 先看规范与 README，再看实现。
2. 优先看可复用架构，不直接照搬大体量实现。
3. 先借鉴接口、目录、数据流、调度、记忆与工具调用方式。
4. 遇到重复能力，优先复用参考仓库中的成熟方案。

## 重点关注项
- MCP：协议、SDK、server/client 结构、工具调用边界。
- Mem0 / GraphRAG：短期与长期记忆、图谱化知识整理。
- LiteLLM / FreeLLMAPI：模型路由、fallback、key 管理、OpenAI 兼容。
- OpenHands / Claude Code / Codex CLI：终端代理、工具执行、任务编排方式。
- miclaw_api_bridge：MiClaw 与 API 桥接方式。
- OpenClaw：整体平台化、插件、skills、执行层组织。

## 后续补充
如果后面发现更多可借鉴仓库，可以直接继续放在这个目录下，并在此处追加说明。
