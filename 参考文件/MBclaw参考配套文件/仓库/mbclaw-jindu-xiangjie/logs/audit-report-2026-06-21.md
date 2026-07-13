# 完整审计报告 — 2026-06-21

## 审计方法
- 逐文档对照 11 份设计文档 (01-vision ~ 11-implementation-status + zh/)
- 逐函数审查 37 个 Kotlin 源文件
- 10 轮 pass，每轮不同维度

## 发现的偏离 (42处)

### 01-vision.md (3处)
| # | 需求 | 实际 | 严重度 |
|---|------|------|--------|
| 1 | Project DNA 渐进更新(增量合并) | 只更新 timestamp | 高 |
| 2 | 经验总结(从过往对话提炼) | 只做关键词,不提炼经验 | 中 |
| 3 | 后续计划(next_plans) | 字段永远是[] | 中 |

### 02-architecture.md (3处)
| # | 需求 | 实际 | 严重度 |
|---|------|------|--------|
| 4 | Session Complete 触发总结+关键词+DNA | sessionCompleteFullFlow 调了但总结不调LLM | 高 |
| 5 | jieba 分词+TF-IDF | 自写简易分词 | 中 |
| 6 | 搜索跨所有维度(项目/会话/消息/总结/关键词) | 只搜 memory 表 | 高 |

### 06-three-tier-client.md (4处)
| # | 需求 | 实际 | 严重度 |
|---|------|------|--------|
| 7 | 辅助语音唤醒(通过小爱打开) | VoiceService 不调小爱 | 高 |
| 8 | Termux+Python+FastAPI 本地服务 | LocalFastAPI 存在但 UI 无入口 | 中 |
| 9 | Magisk 模块+开机自启 | BootReceiver 有,无 Magisk 模块 | 中 |
| 10 | 云端同步 SQLite↔服务器 | SyncService push/pull 是空函数 | 高 |

### 07-lessons-learned.md (1处)
| # | 需求 | 实际 | 严重度 |
|---|------|------|--------|
| 11 | 搜索要跨所有维度 | 只搜 memory 表 | 高 |

### 08-openclaw-reference.md (3处)
| # | P0需求 | 实际 | 严重度 |
|---|--------|------|--------|
| 12 | Memory Flush (压缩前保存到磁盘) | 完全缺失 | 极高 |
| 13 | Dreaming 提升(短期→长期到MEMORY.md) | dream() 只生成文本,不写入 | 极高 |
| 14 | JSONL Session Transcript | TranscriptLogger 有但非per-session | 中 |

### 09-mbclaw-full-vision.md (8处)
| # | 项目 | 实际 | 严重度 |
|---|------|------|--------|
| 15 | P1 thinking字段 | DB有列但聊天不写入 | 高 |
| 16 | P3 git commit+tag | 只写DB,没做 git | 中 |
| 17 | P5 Key1→Key2→Key1 循环1-6次 | 只做一次review | 极高 |
| 18 | P10 反思模板5字段 | 只有findings | 高 |
| 19 | P11 工具embedding | 无 | 高 |
| 20 | P12 模型能力web搜索评分 | 用静态分 | 中 |
| 21 | P13 回滚检测 | 完全缺失 | 中 |
| 22 | P4 多方案并行 | auto_decide 极简 | 中 |

### 10-memory-system-blueprint.md (20处)
| # | 蓝图 | 实际 | 严重度 |
|---|------|------|--------|
| 23 | 2.1-2.2 users/projects 表 | 客户端无 | 低 |
| 24 | 2.3 session_id INTEGER | 客户端用 TEXT | 低 |
| 25 | 4.1 Step1 generate_summary | 取前60字,不调LLM | 高 |
| 26 | 4.1 Step3 DNA增量合并 | 覆盖式,非增量 | 高 |
| 27 | 4.1 Step7 semantic_similarity | keyword_overlap | 高 |
| 28 | 4.1 Step9 old_dna vs new_dna | 只做关键词匹配 | 高 |
| 29 | 4.1 Step10 5字段反思 | 只有findings+problems | 高 |
| 30 | 4.3 checkpoint save/restore | AgentLoop未接入 | 高 |
| 31 | 4.4 4维度评分 32/40阈值 | 单次review | 极高 |
| 32 | 4.5 反思模板+去重+冲突协商 | 简单关键词 | 高 |
| 33 | 4.6 L1/L2/L3 工具索引 | 无L2标签匹配/L3向量 | 高 |
| 34 | 4.7 模型能力评分(w1*coding+w2*reasoning) | 静态简单权重 | 中 |
| 35 | 5 embedding cache | 有文件但未填入向量 | 中 |
| 36 | 5 scheduler 空闲调度 | 简化为定时清理 | 低 |
| 37 | 6 topic_tree.py ORM | 用直接SQL代替ORM | 低 |
| 38 | 7.1 树状分类伪代码 | 偏离算法 | 高 |
| 39 | 7.2 breakthru detection伪代码 | 偏离算法 | 高 |
| 40 | 7.3 prefetch伪代码 | L3未真调用embedding API | 中 |
| 41 | 7.4 模型优化伪代码 | 简化版 | 中 |
| 42 | 7.5 回滚检测伪代码 | 完全缺失 | 中 |

## 真实完成度评估

| 层级 | 声称 | 实际 |
|------|------|------|
| 后端 Python (MBclaw-Lite) | 33/34 97% | 代码存在,未部署 |
| Android 客户端 LLM对话 | 100% | ~80% (可用) |
| Android 客户端 31工具 | 100% | ~60% (部分需Shizuku) |
| Android Hermes记忆 | "100%" | ~15% (概念验证) |
| Android Agent Runtime | "100%" | ~5% (只有AgentLoop骨架) |
| Android 蓝图15表 | "完整" | ~30% (表建了,逻辑不全) |
| Root 系统通道 | "100%" | ~40% (su可用,缺Magisk) |
