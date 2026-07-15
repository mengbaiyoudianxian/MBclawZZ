# MBclawZZ Agent Memory

## 根目录
- 强制工作区：`/tmp/openhands-sandboxes/MBclawZZ/`。
- 禁止使用会话隔离副本路径（例如 `/tmp/openhands-sandboxes/<session>/MBclawZZ/`）作为主工作区。
- 工作根：`/tmp/openhands-sandboxes/MBclawZZ/`。
- 所有后续操作默认基于此根目录。

## 当前资产判断
- `参考文件/GitHub精品参考`：外部开源参考仓库集合。
- `参考文件/MBclaw参考配套文件`：MBclaw 自身相关参考与配套材料。
- `1-母体端`：母体核心设计与运行时。
- `2-后端`：控制面板、sub2api、母体后端、APK 服务后端。
- `3-APK端`：Android/手机端相关。
- `4-总览端`：资产总览、进度、矩阵、研究记录。
- `5-杂项端`：临时实验、待归类、废弃观察、日志残留。
- `6-交接工作区域`：交接、待办、风险、未完成事项。

## 保留优先级
1. `sub2api` 相关
2. `openclaw` 本体与记忆相关
3. `openhands` 相关
4. `mbclaw-mother` 主线
5. 其余参考仓库按需保留

## 约束
- `MBclaw-Server` 当前活跃模型入口链已收口到 `server_app.sub2api_client.Sub2APIClient`；同时已把活跃入口模块的 `app.*` 旧命名空间导入改成 `server_app.*`，避免运行时找不到包。
- 不随意删除未确认的主线资产。
- 不使用复制替代移动。
- 归档与参考必须区分。
- 对外输出前先形成可复用总结。
- 当前已确认：GitHub 账号 `mengbaiyoudianxian` 的主要仓库已盘点，最新主线仓库为 `mbclaw-mother`；`MBclawZZ` 本地目录主要是骨架与文档层，没有业务代码。
- `必读大纲.md` 已包含分篇结构，且已写入 `sub2api` 的整理原则章节；后续重点是继续收敛职责边界、补足未完成事项，而不是新增无关资料。
- 当前本地可复用重点：`4-总览端`、`6-交接工作区域`、`参考文件`、`归档文件`，适合作为后续接手总入口。
- 2026-07-15：`repo: upload full workspace state` 首次推送被 GitHub Push Protection 拦截，原因是 `参考文件/GitHub精品参考/sub2api` 里带入了真实 Google OAuth Client ID/Secret。后续若上传参考仓库快照，优先先做凭据去敏，再推送，避免再次卡在 secret scanning。
