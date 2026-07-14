# MBclaw Mother Runtime Engineering Bible

Version: Draft v0.2
Status: Formal TOC + Part I Expanded
Scope: Mother Runtime engineering bible for the next year of development

---

## 文档使用说明

这不是 README。
这不是宣传稿。
这不是项目介绍。

这份文档的任务只有一个：在不依赖口头补充的前提下，为 MBclaw Mother Runtime 后续至少一年的研究、设计、拆解、实现、评审、验收提供统一工程规范。

它必须回答四个问题：
1. 为什么这样设计。
2. 为什么不用别的方案。
3. 成熟开源项目分别提供了什么。
4. MBclaw 最终如何融合并落地。

当前版本处理两件事：
- 给出更精炼的正式目录版（Formal TOC）。
- 正式开始扩写 Part I：宪法级原则。

---

# Formal Table of Contents

## Part I. 宪法级原则
1. 文档定位与边界
2. 顶层设计原则
3. 设计方法论

## Part II. 地基与全局关系
4. 系统总分层
5. 三层核心关系图
6. 运行时全局调用链

## Part III. Mother Runtime 主体研究
7. Runtime 总体定位
8. Governor
9. Planner
10. Scheduler
11. Worker Runtime
12. Context Engine
13. Event Kernel
14. State Machine
15. Prompt Runtime
16. Checkpoint / Recovery
17. Streaming Runtime

## Part IV. Mother 的关键外围模块
18. Gateway
19. Memory System
20. Capability Registry
21. Tool Runtime
22. Agent Collaboration Runtime
23. Observation / Reflection / Evolution

## Part V. sub2api 作为第一层地基的工程研究
24. Why sub2api
25. sub2api Architecture Research
26. Mother → sub2api Integration Design

## Part VI. Control Center Engineering Research
27. Control Center Position
28. Control Center API Surface

## Part VII. 客户端与桥接层研究
29. Android / MiClaw
30. Windows / Linux / Web
31. APK Bridge / External Bridge

## Part VIII. 数据层与基础能力
32. Data Layer
33. Knowledge Graph / Recall / Archive
34. Security / Monitoring / Benchmark / Testing

## Part IX. 开源项目研究总表
35. Runtime-family Comparison
36. Borrow / Reject Matrix

## Part X. GitHub Engineering Structure
37. Final Repository Layout
38. Directory-by-Directory Future Files

## Part XI. 开发任务拆解
39. Phase Plan
40. Module-level Task Breakdown
41. Dependency / Complexity / Priority Matrix

## Part XII. Final Design & Comparison
42. Final Design Decisions
43. Comparison Tables
44. Acceptance Rules
45. Work Handoff Standard

## Appendix
A. 术语表
B. 状态机图索引
C. 事件模型索引
D. 接口模型索引
E. 开源项目链接索引
F. 风险清单索引
G. 待决策问题索引

---

# Part I. 宪法级原则

> 这一部分不是背景介绍，而是整个 MBclaw Mother Runtime 的施工宪法。  
> 后续任何章节、目录、接口、实现，只要与本部分冲突，都必须优先修改实现，而不是稀释原则。

## Chapter 1. 文档定位与边界

### 1.1 为什么需要 Engineering Bible

MBclaw 后续最大的风险，不是代码量不够，而是结构先天走样。

如果没有一份真正具备约束力的工程规范，项目很容易滑向以下坏结果：

1. 边界漂移。今天把调度写在 Mother，明天把同一套调度又写进控制面板，后天再在端侧补一个简化版，最后谁都能调度，谁都说自己是入口。
2. 词语一致，结构不一致。表面都说“用 sub2api 做模型入口”，实际却在 Mother 里继续塞 provider 选择逻辑，在客户端里继续保留旧 TokenPool 假壳。
3. 研究与实现脱节。研究材料越来越多，但没有形成“借什么、不借什么、为什么”的稳定判定。
4. 接手成本过高。后续任何 AI 或开发者都必须靠补充聊天才能继续施工，这意味着系统并没有形成可继承的工程规范。

Engineering Bible 的意义，就是把这些原本漂浮在对话里的判断固定为长期有效的工程地基。

它存在的原因不是“写得更正式”，而是为了让 MBclaw 形成以下能力：
- 可设计
- 可拆解
- 可复核
- 可接手
- 可扩写
- 可回滚
- 可追责

换句话说，这份文档不是为“现在好看”服务，而是为“未来不烂掉”服务。

### 1.2 这份文档解决什么问题

这份文档主要解决六类问题：

#### 1.2.1 地基关系问题
必须明确：
- sub2api 是第一层地基
- Mother 是第二层地基
- Control Center 建在两层地基之上
- Client / Bridge / Platform 再建在其上

这不是命名偏好，而是依赖方向。谁能依赖谁、谁不能反向定义谁，必须在文档里先定死。

#### 1.2.2 模块边界问题
必须明确每个模块：
- 为什么存在
- 负责什么
- 不负责什么
- 输入是什么
- 输出是什么
- 生命周期是什么
- 故障时如何恢复

没有这些定义，后续编码一定会自然滑向“谁方便谁顺手做了”，最后边界完全失效。

#### 1.2.3 开源借鉴问题
MBclaw 不应该重新发明所有轮子。但“不重新发明轮子”不等于“把别人的实现生吞”。真正困难的是：
- 哪些能力应该直接复用
- 哪些能力应该裁剪后复用
- 哪些能力根本不适合引入
- 哪些地方必须自己做

#### 1.2.4 工程顺序问题
很多系统不是死在能力不够，而是死在顺序错误。例如：
- 地基没定就先做控制面板
- 状态机没定就先做多端同步
- 调度边界没定就先做模型选择 UI
- 事件规范没定就先做模块通信

#### 1.2.5 任务拆解问题
真正可执行的工程规范，必须能自然落到：
- Phase
- Milestone
- Task
- SubTask
- Checklist

#### 1.2.6 验收问题
MBclaw 不能靠“差不多能跑”来验收。验收至少要过三关：
1. 设计是否自洽
2. 实现是否符合设计
3. 用户是否明确确认这项能力可以进入已完成区

### 1.3 这份文档不解决什么问题

为了防止文档膨胀，这份文档也必须明确不解决什么：

- 不解决宣传问题
- 不解决快速上手问题
- 不替代代码注释
- 不替代日常任务看板
- 不替代专题迁移文档

例如 sub2api 专题迁移表、控制面板专题、APK 视觉交互专题，仍然需要独立文档。这份 Bible 负责定义总规则和最终方向，不负责吞掉所有细节专题。

### 1.4 适用范围

本规范适用于以下层级：
- Mother Runtime
- Mother 周边核心模块
- sub2api 与 Mother 的集成边界
- Control Center 的架构边界
- Client / Bridge 与 Mother 的接口预留
- 长期演化相关的数据层、观测层、恢复层、评测层

更具体地说，凡是涉及以下事项，必须优先回到本规范：
- 新目录设计
- 新模块立项
- 新接口预留
- 跨模块调用
- 运行时改造
- 调度逻辑改造
- 状态机改造
- 记忆层设计
- 控制面板增量设计
- 客户端 API 预留

### 1.5 与《必读大纲.md》的关系

《必读大纲.md》是总施工宪法，覆盖 MBclawZZ 整个工作区。

本 Bible 则是其中更窄、更深的一层：
- 《必读大纲.md》回答：整个 MBclaw 总体应该长成什么样
- 本 Bible 回答：Mother Runtime 这一条主线在工程上到底应该怎么长

因此两者关系不是互斥，而是：
- 大纲负责总边界
- Bible 负责主线深挖

如果两者冲突：
1. 先检查是不是 Bible 写偏了大纲
2. 若是，则 Bible 必须回调
3. 若不是，再判断是不是大纲过于粗，需要回补总纲

### 1.6 与其他文档的关系

交接文档解决的是“当前做到哪里了”。Bible 解决的是“为什么应该这样做，以及接下来必须怎么做”。

专题矩阵解决的是“单个主题如何迁移、如何对比、如何收口”。Bible 解决的是“这些专题最后怎么被统一纳入 Mother Runtime 工程体系”。

真实代码仓是实现载体，Bible 是实现之前的工程定义。因此任何真实代码改动，都应该能回答一句话：

> 这次改动对应 Bible 的哪一章、哪一节、哪一个任务拆解点？

如果回答不出来，说明施工很可能已经开始漂移。

---

## Chapter 2. 顶层设计原则

### 2.1 sub2api 是第一层地基

这是整个 MBclaw 当前最重要的结构前提。Mother 不应该承担资源治理。

Mother 的职责是目标理解、流程编排、上下文组织、能力调度、结果回传。它应该知道：
- 我现在需要什么能力
- 需要什么模型特性
- 需要什么上下文预算
- 需不需要 fallback 策略

但它不应该知道：
- 当前哪个 key 健康
- 哪个 provider 现在更稳
- 哪个模型最近限流严重
- 哪个账户正在冷却
- 哪个 fallback 路径成本最低

这些都是第一层地基应该解决的问题，也就是 sub2api 的职责。

如果没有这一层地基，Mother 会自然长出坏结构：
- provider 选择逻辑散在多个文件里
- token pool 历史壳长期不死
- fallback/retry/cooldown 被多处重复实现
- 健康检测与统计失去唯一权威来源

所以这里必须定死：
- sub2api 是唯一模型入口地基
- 所有模型资源治理都先落到 sub2api
- Mother 不得再并行维护第二套入口实现

### 2.2 Mother 是第二层地基

Mother 建在 sub2api 之上，但不是一层薄壳。

它是第二层地基，意味着它承接的是系统执行中枢，而不是简单业务层。它至少承担：
- 目标理解
- 任务拆解
- 计划修订
- 上下文注入
- 记忆召回
- 工具选择
- 子任务派发
- 结果汇总
- 失败恢复
- 经验记录

换句话说，sub2api 负责“资源去哪拿”，Mother 负责“事情怎么做完”。

如果把 Mother 写成只会转发请求的中间层，那不是第二层地基，而只是代理壳；如果把 Mother 写成同时管理 key、provider、fallback、冷却、计费，那它又会吞掉第一层地基的职责。

### 2.3 控制面板建立在两层地基之上

控制面板不是地基。

控制面板的职责是：
- 观察地基状态
- 管理地基配置
- 暴露管理接口
- 为端侧提供统一管理入口

它不应该反过来定义：
- sub2api 应该怎么调度
- Mother 应该怎么组织上下文
- Gateway 应该怎么归一输入

如果控制面板先行，最容易出现的坏结构是：
- 为了 UI 容易做，先把底层接口定死
- 为了端侧方便调，要求地基层长期兼容旧字段
- 为了统计图好看，把真正的状态机边界打散

正确顺序必须是：
1. 先定 sub2api 边界
2. 再定 Mother 边界
3. 再让控制面板建立在两者稳定接口之上
4. 同时为 Android / Windows / Linux / Web 预留 API 与上传接口

### 2.4 Gateway 是唯一平台入口

所有平台输入都必须先经过 Gateway，再进入 Mother Runtime。

Gateway 的意义不是多一层，而是少混乱。只要平台入口不统一，Mother 就会出现：
- 平台特判分支
- 各种 payload 直塞
- 不同平台消息结构混杂
- 上传附件、身份、回复格式在 Runtime 里乱飞

Gateway 的职责是：
- Adapter
- Normalize
- Session
- Identity
- Upload
- Reply

它不负责：
- 规划
- 记忆拼装
- 模型调度
- 工具编排

### 2.5 Runtime 是唯一执行中枢

LLM 不是大脑，Runtime 才是大脑。LLM 只是 Worker。

如果没有 Runtime 这一层，系统会变成：来一条消息、调一次模型、回一段文本。这不叫 Operating System，只叫问答壳。

Runtime 必须成为唯一执行中枢，负责：
- 事件循环
- 状态推进
- 上下文装配
- Worker 调度
- 工具执行
- 回复汇总
- 故障恢复
- 经验回写

### 2.6 记忆、工具、Agent、Runtime 分层

这四层最容易互相吞职责。必须明确：
- Memory 负责存取与召回
- Tool Runtime 负责工具执行与结果回传
- Agent 负责特定工作模式或角色执行
- Runtime 负责把它们编排成一个闭环

所以这里必须坚持：
- Memory 不做规划
- Tool 不做策略
- Agent 不做全局调度
- Runtime 不做长期存储细节

### 2.7 上层兼容下层地基，不反向兼容

这条原则必须写死，因为它直接决定未来一年代码会不会继续烂下去。

正确兼容方向是：
- Mother 兼容 sub2api
- Control Center 兼容 sub2api + Mother
- Client / Bridge / Web 兼容 Control Center / Mother 的公开接口

错误兼容方向是：
- 让 sub2api 为 Mother 历史字段兜底
- 让 Mother 为旧 TokenPool 壳长期保留转发语义
- 让 Gateway 为端侧临时写法永久保留脏接口

向下兼容可以有，反向兜底不能成为长期结构。否则所有历史壳都会以“兼容”为名永久活着，系统永远没有真正收口的一天。

### 2.8 接口先行，禁止跨层直连

模块之间的稳定关系，必须通过接口体现，而不是靠默认 import 路径约定。

接口先行的意义，不是官僚主义，而是让未来的替换、回放、测试、并行开发成为可能。

原则固定为：
Caller → API → Service → Runtime → Result

能不跨层，就绝不跨层。

### 2.9 事件优先于散乱调用

MBclaw 是一个长期运行系统，不是一个单过程脚本。

长期运行系统要解决的，不只是“现在能调通”，而是：
- 谁触发了谁
- 哪个状态变了
- 是否能重放
- 是否能追责
- 是否能恢复

事件优先的意义，在于把系统行为从“隐式调用链”变成“可追踪状态变化链”。

### 2.10 先研究、再设计、后编码

MBclaw 的复杂度决定了：
- 研究不是附属品
- 比较不是可选项
- 设计不是总结稿

正确顺序必须是：
1. 研究业内成熟方案
2. 做借鉴/排除判断
3. 产出 MBclaw Final Design
4. 再拆任务
5. 最后才进入编码

只要顺序倒了，后面一定要返工。

---

## Chapter 3. 设计方法论

### 3.1 六段法：Position / Responsibilities / Architecture / Engineering / Research / Final Design

MBclaw 后续所有模块设计，都必须至少用这六段法展开。

#### 3.1.1 Position
回答模块为什么存在：
- 没有它会怎样
- 为什么不能并到别处
- 为什么不是另一个模块来承担
- 这个模块在行业里的共性价值是什么

#### 3.1.2 Responsibilities
列清楚所有职责，不许模糊。

例如 Memory 不能只写“负责记忆”，必须拆成：
- Working Memory
- Conversation Memory
- Project Memory
- Decision Memory
- Knowledge Memory
- Experience Memory
- Capability Memory
- Observation Memory
- User Memory
- Evolution Memory
- Recall
- Compression
- Merge
- Archive
- Recovery
- Ranking
- Injection

#### 3.1.3 Architecture
必须不断拆，直到不能再拆。

例如 Scheduler 不能只停在“调度器”，而要继续拆：
- Worker Selector
- Provider Selector
- Token Selector
- Retry Engine
- Fallback Engine
- Budget Engine
- Streaming Coordination
- Queue
- Cancellation
- Health Check
- Circuit Breaker
- Rate Limit
- Scoring
- Benchmark

#### 3.1.4 Engineering
对每个功能，必须分析实现方式，而不是直接写“最后采用”。

至少要比较：
- 业内常见实现路线
- 每条路线的优点
- 每条路线的缺点
- 适合什么规模
- 不适合什么场景
- 哪些能照搬，哪些要裁剪

#### 3.1.5 Research
Research 不是贴 GitHub 链接，而是要回答：
- 这个项目值不值得研究
- 值得借哪些目录、类、设计
- 哪些地方不能借
- 为什么不能借
- 它解决了什么，而 MBclaw 当前缺什么

#### 3.1.6 Final Design
Final Design 不是“综合来说采用方案 A”，而是必须明确：
- 来自谁
- 保留什么
- 删除什么
- 新增什么
- 为什么是这个组合

### 3.2 每个模块必须拆到不能再拆

“模块拆解不够”是很多系统后续失控的根本原因。

只要拆得不够细：
- 职责会重叠
- 对照会失真
- 任务拆解会失真
- 复杂度评估会失真

因此任何模块进入设计时，都必须问自己：
- 里面是不是还混了不同生命周期的东西？
- 里面是不是还混了不同状态机的东西？
- 里面是不是还混了不同依赖方向的东西？
- 里面是不是还混了不同性能瓶颈的东西？

只要答案是“是”，就继续拆。

### 3.3 每个模块必须给出成熟项目对照

MBclaw 不允许只写“我们自己的设计”。

每个核心模块都必须对照至少一类成熟项目，例如：
- Runtime：OpenHands / Claude Code / Codex CLI
- Router / Fallback / Health：LiteLLM / FreeLLMAPI / sub2api
- Memory：Mem0 / GraphRAG / NotebookLM-style systems / WorkBuddy-like graph systems
- Gateway / Bridge：OpenClaw / GUI automation / bridge runtimes

### 3.4 每个模块必须说明为什么不用其他方案

这条经常比“为什么采用当前方案”更重要。

真正决定架构质量的，不只是你选了什么，而是你拒绝了什么。例如：
- 为什么不用 Runtime 直接调用模型
- 为什么不用 Gateway 直接拼上下文
- 为什么不用 Control Center 直接驱动资源层
- 为什么不用 TokenPool 历史壳继续补丁前进

### 3.5 每个模块必须产出 GitHub 工程结构与任务拆解

设计如果不能落到目录与任务，就还不是真正可执行的工程规范。

因此每个模块最后都必须给出：
- 推荐目录位置
- 未来文件结构
- 哪些目录来自第三方思路
- 哪些目录必须 MBclaw 自主维护
- Phase / Milestone / Task / SubTask / Checklist

---

## Part I 当前结论

到这里，Part I 已经把后续所有章节必须遵守的基础纪律定死：

1. sub2api 是第一层地基。
2. Mother 是第二层地基。
3. Control Center 建在两层地基之上。
4. 兼容方向只能是上层适配下层，不能反向兜底。
5. Runtime 不是 LLM 包装层，而是执行中枢。
6. 所有模块设计都必须经过研究、比较、拆解与最终融合判断。

如果后续章节偏离这六条，优先修改章节，不修改原则。

---

## 待扩写队列

下一步建议按以下顺序展开：
1. Part II. 地基与全局关系
2. Part V. sub2api 作为第一层地基的工程研究
3. Part III. Mother Runtime 主体研究（先 Chapter 7 与 Chapter 10）
4. Part VI. Control Center Engineering Research

---

# Part II. 地基与全局关系

## Chapter 4. 系统总分层

### 4.1 为什么必须按地基顺序建设

MBclaw 不能采用“哪个需求最急先做哪个”的自然生长方式，因为这类系统一旦先长上层，再补下层，最终一定会出现接口反向塑形地基的问题。

正确顺序必须固定为：

1. sub2api
2. Mother
3. Control Center
4. Client / Bridge
5. Platform
6. Ecosystem

原因不是形式美观，而是依赖方向单一。

- sub2api 先定资源治理边界
- Mother 再定执行中枢边界
- Control Center 再基于前两层暴露管理接口
- 客户端再基于公开接口接入
- 平台层再整合账号、同步、官网、开发者中心
- 生态层最后才做插件、市场、工作流

如果顺序倒过来，系统会变成“谁先实现谁定义结构”，最终没有真正稳定的地基。

### 4.2 第一层地基：sub2api

sub2api 是资源层，不是业务层。

它解决的是：

- key 管理
- provider 管理
- model registry
- routing
- retry
- fallback
- cooldown
- health
- stats
- admin
- OpenAI-compatible entry

它不解决的是：

- 用户目标理解
- 任务拆解
- 记忆拼装
- 工具编排
- 平台消息归一
- 端侧交互策略

sub2api 之所以必须先于 Mother 建立，不是因为它“更底层”，而是因为 Mother 的执行质量依赖它提供一个稳定、统一、可治理的模型资源面。

只要 sub2api 没定，Mother 的 Scheduler 就会天然滑向资源治理，进而把本该属于第一层地基的逻辑带进第二层地基。

### 4.3 第二层地基：Mother

Mother 不是资源层，也不是 UI 层。它是执行中枢层。

它建立在 sub2api 之上的原因，是因为它需要把“要做什么”与“资源从哪里来”彻底拆开。

Mother 的工作应该集中在：

- 目标理解
- 任务分解
- 上下文组织
- 记忆注入
- 工具选择
- Agent 协作
- Worker 调度
- 回复合成
- 经验沉淀

Mother 不应该继续维护：

- 独立 token pool
- 独立 provider selector
- 独立 cooldown engine
- 独立 account health state
- 独立 usage stats authority

Mother 可以决定策略，但不拥有资源治理主权。

### 4.4 第三层：Control Center

Control Center 的存在，是为了统一管理，而不是反向定义架构。

它建立在前两层地基之上后，才有资格提供：

- 总览视图
- 服务状态
- 日志检索
- 配置管理
- 用户与设备视图
- 管理 API
- 数据上传接口
- 状态查询接口
- 鉴权接口
- 资源读取接口

这里最重要的一条纪律是：

> 控制面板永远只能消费并组织地基层公开接口，不能倒逼地基层为了历史页面、历史字段、历史端侧写法去反向兼容。

### 4.5 第四层：客户端与桥接层

客户端不是核心逻辑所在地，而是触达与执行端。

因此 Android、Windows、Linux、Web、APK Bridge 这些层，不应该把自己的临时需求直接压进 Mother 或 sub2api 的内部实现。

它们必须通过预留接口接入：

- 管理 API
- 上传 API
- 状态 API
- 鉴权 API
- 资源查询 API

越靠近端侧，越应该避免定义核心结构。

### 4.6 第五层与第六层：平台与生态

平台层和生态层必须后置，不是因为它们不重要，而是因为它们天然依赖前面所有层级的稳定接口。

如果前面三层没有定死，平台层做得越快，返工成本越大；生态层做得越早，污染主线的概率越高。

所以平台与生态的基本纪律是：

- 不反向塑造 Runtime
- 不反向塑造 sub2api
- 不反向定义 Control Center 的内部结构
- 必须建立在稳定接口之上

---

## Chapter 5. 三层核心关系图

### 5.1 单向依赖图

正确依赖关系应固定为：

Client / Bridge / Platform
↓
Gateway / Control Center
↓
Mother Runtime
↓
sub2api

这里有两个关键点：

1. Control Center 不在 Mother 下面，它在管理关系上横跨 Mother 与 sub2api。
2. Gateway 是平台入口，不是资源入口；sub2api 是资源入口，不是平台入口。

### 5.2 三层核心分别拥有什么主权

#### sub2api 的主权
- 模型资源治理主权
- key/provider/model 生命周期主权
- routing/fallback/health/stats 主权

#### Mother 的主权
- 任务执行与编排主权
- 上下文、记忆、工具协作主权
- Worker 调度与回复组织主权

#### Control Center 的主权
- 管理聚合主权
- 观测与配置组织主权
- 对端侧暴露管理面与状态面的主权

谁也不能越权吞掉别人的主权。

### 5.3 为什么不能让控制面板反向定义地基

因为一旦 Control Center 先行，工程上会发生三件坏事：

1. 接口为了页面方便而不是为了地基稳定被设计。
2. 历史字段永久保留，地基层失去收口机会。
3. 端侧与管理面的偶然需求被误当成系统级约束。

所以必须有一条硬规则：

- 页面为接口服务
- 接口为地基服务
- 地基不为页面临时便利让步

### 5.4 为什么 Mother 只能兼容 sub2api，不能反过来

因为 Mother 是第二层地基，sub2api 是第一层地基。

第二层地基向第一层地基收敛，是正常依赖关系；第一层地基反向为第二层地基的历史壳做兜底，则会让第一层失去独立性。

一旦 sub2api 需要长期维护 Mother 历史调用壳：

- sub2api 内部结构会被污染
- 资源层 API 会被迫保留业务层语义
- 后续 Control Center 也会被拖进历史兼容泥潭

因此：

- Mother 可以改
- Control Center 可以改
- 客户端可以改
- sub2api 不以“继续兼容历史调用壳”为主要目标

### 5.5 三端与 Web 的接口预留原则

Android、Windows、Linux、Web 不是四套独立架构，它们只是四类接入视图。

所以接口预留的目标不应是“每端一套专用后门”，而应是：

- 统一管理 API
- 统一上传 API
- 统一状态 API
- 统一鉴权 API
- 统一资源查询 API

差异应该留在 Adapter / Client 侧，不应该倒灌进地基层。

---

## Chapter 6. 运行时全局调用链

### 6.1 正常主链

MBclaw 的标准主链应该是：

Platform Input
→ Gateway
→ StandardMessage
→ Mother Runtime
→ Context / Memory / Tool / Agent / Scheduler
→ sub2api
→ Worker Result
→ Mother Reply Assembly
→ Gateway Reply
→ Platform Output

这条链必须尽量单向，不允许在主链中间插入多套并行入口。

### 6.2 Gateway 之后必须只看到标准对象

Mother Runtime 不应该直接看到：

- 原始 QQ payload
- 原始微信 payload
- 原始 Web form body
- 原始端侧 UI 事件对象

它应该只看到 StandardMessage 以及 Runtime 所需的标准上下文对象。

这条规则的意义，是把平台差异永远挡在 Gateway 之前。

### 6.3 Runtime 内部的调用链

进入 Runtime 后，标准链路应继续收束为：

StandardMessage
→ Goal Understanding
→ Planning
→ Context Injection
→ Memory Recall
→ Tool / Agent Selection
→ Worker Scheduling
→ Model Request via sub2api
→ Result Merge
→ Reflection / Experience Writeback
→ Reply Assembly

这里最重要的不是“顺序一模一样”，而是每一阶段都应该有独立边界，不要把多个阶段揉成一个大函数或一个大模块。

### 6.4 Model Request 必须经过 sub2api

Mother Runtime 可以决定：

- 此时是否需要模型
- 需要什么能力
- 需要什么上下文预算
- 需要什么工具联动

但它不能直接决定：

- 用哪个 key
- 切哪个 provider
- 走哪个 cooldown 状态
- 记哪套 resource stats

这些都必须经由 sub2api。

所以在调用链上，任何“Mother 直接请求 provider”的历史路径，原则上都应视为临时遗留，而不是未来主线。

### 6.5 Reply 只能由 Mother 汇总，平台由 Gateway 适配

sub2api 不能负责平台回复。

Tool Runtime 不能直接对平台发消息。

Client 也不能直接替 Mother 决定回复策略。

必须固定：

- Mother 负责生成统一回复结果
- Gateway 负责把统一回复结果适配到不同平台

这样才能保证：

- 业务逻辑统一
- 平台适配独立
- 多端扩展不污染 Runtime

### 6.6 Observation、Reflection、Handoff 必须进入主链尾部

MBclaw 不是“一次调用完就结束”的系统，所以主链尾部不能只停在 Reply。

Reply 之后至少还要有：

- Observation
- Reflection
- Experience Writeback
- Handoff Artifact Update（必要时）

特别是长任务、复杂任务、跨会话任务，交接不是附属动作，而是主链尾部的正式输出之一。

没有这一步，系统就会不断重复学同样的课。

---

## Chapter 45. Work Handoff Standard

### 45.1 为什么工作交接标准必须独立成章

绝大多数工程规范把“交接”写成附录，结果就是大家都觉得这只是礼貌动作，不是正式产物。

MBclaw 不能这样。

对 MBclaw 来说，交接标准必须独立成章，因为它直接决定：

- 下一个 AI 能不能无痛接手
- 下一个窗口是不是要重新盘点一遍
- 当前窗口的成果是不是可复用
- 失败方案有没有被明确沉淀
- 主线是不是会因为换窗口而断裂

所以交接不是“顺手写几句总结”，而是正式输出物。

### 45.2 什么情况下必须交接

出现以下任一情况，必须产出正式交接：

1. 会话准备结束，但主线未完。
2. 已完成一个阶段性突破，需要冻结中间结论。
3. 已修改目录、边界、主线口径、迁移方向。
4. 已定位关键失败路径，需要防止后续重复踩坑。
5. 已形成可继续施工的任务拆解。
6. 需要把当前窗口结果交给另一个 AI / 另一个子会话 / 下一个开发窗口。

### 45.3 什么不算合格交接

以下都不算：

- “大概做了这些”式口语总结
- 只说改了什么，不说为什么
- 只说成功方案，不说失败方案
- 只贴文件名，不说明文件价值
- 只说主线，不说风险
- 只说未来要做什么，不说当前做到哪里

交接如果无法降低下一个窗口的理解成本，就不是交接，只是聊天尾声。

### 45.4 正式交接必须包含的内容

正式交接至少必须包含九块：

#### 45.4.1 一句话结论
当前主线走到哪，最核心的判断是什么。

#### 45.4.2 当前状态
- 当前工作区
- 当前默认分支
- 当前最新提交
- 是否已推送
- 是否还有未提交改动

#### 45.4.3 已完成内容
必须列具体，不允许写“完成若干优化”。

#### 45.4.4 当前主线口径
例如：
- sub2api 是第一层地基
- Mother 是第二层地基
- Control Center 建在两层地基之上
- 兼容方向只能上层适配下层

#### 45.4.5 未完成内容
必须写清：
- 还没做什么
- 为什么还没做
- 卡在哪
- 下一步从哪开始

#### 45.4.6 风险点
必须明确：
- 哪些路径容易误判
- 哪些目录容易混淆
- 哪些历史材料不能当现行主线
- 哪些代码改动暂时不能带上去

#### 45.4.7 失败方案与禁止重试项
这块尤其重要。

必须明确写出：
- 哪些思路已经验证偏航
- 为什么偏航
- 后续不要再按什么方式做

#### 45.4.8 最短接手路径
必须告诉下一个窗口：
- 先看哪几个文件
- 先执行什么检查
- 下一刀从哪个模块切入

#### 45.4.9 验收与完成状态
必须说明：
- 哪些只是本地完成
- 哪些已经提交
- 哪些已经推送
- 哪些已经过用户确认

### 45.5 交接文件的推荐结构

推荐统一采用以下结构：

1. 一句话结论
2. 当前状态
3. 已完成的关键工作
4. 当前已形成的核心口径
5. 已同步的结构变化
6. 当前最值得继续做的事
7. 风险点
8. 给下一窗口的最短接手方式

如果是更大型阶段交接，可增加：

- 失败方案清单
- 依赖与阻塞清单
- 已验证但暂不推进的方向
- 未提交改动清单

### 45.6 交接标准与文件标准的关系

交接必须同时满足：

- 能被人读
- 能被 AI 读
- 能被下一窗口直接执行

这意味着交接不能只写抽象结论，还必须带：

- 文件路径
- 仓库路径
- 分支状态
- 提交状态
- 下一步入口

缺任何一项，交接都会打折扣。

### 45.7 交接标准与默认分支同步标准

如果一个交接已经代表当前主线判断，原则上应尽快进入默认分支，而不是长期漂在本地。

默认分支同步前必须检查：

1. 这次提交是否只包含目标内容。
2. 是否混入未完成代码壳。
3. 是否把临时缓存、实验文件、未确认代码一并带上。
4. 是否会把错误口径写进主线。

交接类提交允许快，但不允许脏。

### 45.8 用户确认在交接中的地位

对 MBclaw 来说，真正的完成不只是“自己觉得写完了”，而是：

- 工程上已经自洽
- 产物已经可接手
- 用户明确认可当前阶段可作为下一步地基

也就是说：

- 交接文件可以先写
- 交接提交可以先推
- 但“已完成”标签是否进入主线完成区，仍然以用户明确认可为准

### 45.9 交接章节的最终纪律

后续任何复杂施工，只要会跨窗口，就默认需要正式交接。

不允许再出现：

- 只有聊天记录，没有结构化交接
- 只有目录变化，没有主线口径
- 只有主线口径，没有风险与失败清单
- 只有文件名，没有接手顺序

MBclaw 的交接标准，不是为了文档好看，而是为了让系统具备真正的连续施工能力。

---

## 当前扩写进度

已完成：
- Formal TOC
- Part I. 宪法级原则
- Part II. 地基与全局关系
- Chapter 45. Work Handoff Standard

建议下一步继续：
1. Part V. sub2api 作为第一层地基的工程研究
2. Part III. Mother Runtime 主体研究（先 Chapter 7 与 Chapter 10）
3. Part VI. Control Center Engineering Research
