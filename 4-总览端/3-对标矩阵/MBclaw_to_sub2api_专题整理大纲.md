# MBclaw → sub2api 专题整理大纲

## 1. 目标
把 MBclaw 原先与模型入口相关的能力，按 sub2api 的现有结构重新整理成可落地、可迁移、可接手的专题方案。

本专题不是再维护一套并行 sub2api，而是：
- 以 `Wei-Shaw/sub2api` 为主载体
- 以官方仓库 `Wei-Shaw/sub2api` 为准
- 结合官方演示站、Docker 镜像、以及相关 fork 做实现对照
- 将原模型入口能力映射到 sub2api 的 backend / frontend / tools / skills / docs
- TokenPool 只作为历史参考，不作为需要继续兼容保留的目标实现

## 2. 参考资产
### 2.1 主参考
- 官方仓库：`https://github.com/Wei-Shaw/sub2api`
- 官方演示站：`https://demo.sub2api.org/`
- 官方 Docker 镜像：`https://hub.docker.com/r/yw79641760/sub2api`

### 2.2 次级参考
- `wey-gu/sub2api`
- `moeacgx/sub2api`
- 其他与 sub2api 相关的 fork 或二开版本

### 2.3 本地已克隆资源
- 已克隆远程仓库 `Wei-Shaw/sub2api`

## 3. 模型入口能力分类
### 3.1 能力一：模型入口统一
- 统一上游接入
- 统一标准 API
- 统一请求入口

### 3.2 能力二：调度与路由
- provider 选择
- model 选择
- fallback
- retry
- cooldown
- rate limit 处理

### 3.3 能力三：key 与 provider 管理
- key 增删改查
- provider 配置
- 启用 / 禁用
- 冷却 / 恢复
- 失败状态管理

### 3.4 能力四：统计与健康检测
- 调用量统计
- 成功率统计
- 失败类型统计
- 健康探测
- 最近使用时间
- 最近失败时间

### 3.5 能力五：管理后台
- token 列表
- provider 列表
- 模型列表
- 调度状态
- 冷却状态
- 测试与验证

## 4. sub2api 结构映射
### 4.1 backend
建议承接：
- 模型入口
- 账号 / key / provider 管理
- 路由与 fallback
- 健康检测
- 统计
- admin API

### 4.2 frontend
建议承接：
- 管理面板
- key / provider / group / usage / auth / payment / admin 相关页面
- dashboard 与健康状态页面

### 4.3 tools
建议承接：
- 管理脚本
- 检查脚本
- 数据迁移脚本
- 质量检查脚本

### 4.4 skills
建议承接：
- sub2api-admin 相关技能
- 管理 API 的标准操作手册
- 统一操作步骤与示例

### 4.5 docs
建议承接：
- API 说明
- 管理说明
- 合规与风险说明
- 迁移记录

## 5. 迁移策略
### 5.1 直接照搬
优先直接照搬：
- 明确的 API 形状
- admin 管理动作
- 健康检测思路
- fallback / retry / cooldown 逻辑
- dashboard 的状态展示方式

### 5.2 复用后裁剪
适合复用后裁剪：
- provider 抽象
- key 生命周期
- 统计粒度
- 任务分类
- 管理界面布局

### 5.3 不再并行维护
不再并行维护：
- 第二套 sub2api 后端
- 第二套重复的调度逻辑
- 第二套独立管理台
- 任何以 TokenPool 名义长期保留的旧门面、旧目录、旧接口壳

## 6. 完整迁移表
| 模型入口能力 | sub2api 承接位置 | 处理方式 | 备注 |
|---|---|---|---|
| 统一模型入口 | backend | 直接承接 / 映射 | 以 sub2api 为基础，不为旧 TokenPool 保留兼容壳 |
| provider 路由 | backend | 直接复用 / 裁剪 | 先保留路由主干 |
| fallback / retry | backend | 直接复用 | 作为核心能力保留 |
| cooldown / rate limit | backend | 直接复用 | 与统计联动 |
| key 管理 | backend + frontend | 直接复用 | 管理页面必须可见 |
| provider 管理 | backend + frontend | 直接复用 | 可与 group 体系联动 |
| 健康检测 | backend | 直接复用 | 纳入统计与告警 |
| 统计报表 | backend + frontend | 直接复用 / 裁剪 | 保留关键指标 |
| admin 操作 | skills + frontend | 直接复用 | 优先形成标准操作流 |
| 说明文档 | docs | 直接复用 / 重写 | 保留合规与风险提示 |

## 7. 输出物
1. 专题整理大纲
2. sub2api 功能映射表
3. 保留 / 迁移 / 裁剪 / 归档清单
4. 风险点清单
5. 后续施工顺序
6. 验收标准

## 8. 验收标准
- 能明确说出每项模型入口能力落到 sub2api 的哪里。
- 能明确说出哪些东西直接照搬，哪些需要裁剪。
- 能明确说出哪些能力不再在 MBclaw 侧并行维护。
- 能直接指导后续施工，而不是停留在口头总结。
