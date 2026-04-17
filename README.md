# dao-genesis (道·起源)

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)

> **道生一，一生二，二生三，三生万物。**
> 
> 在智能体（AI Agents）的宇宙中，**复盘与记忆**就是从无知走向有知的“源起（Genesis）”。

`dao-genesis` 是由 `daoAgents` 组织开源的**系统性复盘与记忆管理技能（Prompt & Workflow）**。它为大语言模型（如 Trae 等 AI 辅助编码工具）构建了一个具备自我进化能力的“外脑系统”。

通过结构化的复盘分析与长效记忆管理机制，它能够自动从过往的任务执行、技术决策与交互历史中提取高价值经验，并以 `JSON/Markdown` 形式固化到本地或远端仓库中。

---

## 🌟 核心能力 (Core Capabilities)

- **结构化复盘 (Structured Retrospective)**：自动提取关键元数据、决策链路树、成功/失败教训（红黑榜），并生成可复用的 SOP。
- **项目级双轨记忆 (Storage & Cache)**：
  - `.storage/`：存放需长期保留、可跨设备/团队共享的持久化业务数据（如复盘结论）。
  - `.cache/`：存放可重建的临时数据（如检索索引、摘要缓存），避免污染版本库。
- **多平台追踪闭环 (Cross-Platform Traceability)**：
  - 向上追溯：记录 GitHub / GitLab / AtomGit 的 Issue/PR 链接，随时跳回代码变更现场。
  - 向下穿透：支持将生成的复盘 `review_id` 作为评论写回对应平台的工单系统。
- **极简 Token 控制 (Token Optimization)**：通过按需读取、高度提炼一句话结论、TopK 检索截断等机制，极大降低大模型在长周期下的上下文成本。

---

## 🚀 快速上手 (Quick Start)

### 1. 初始化项目目录
在你的业务项目根目录下，创建供大模型读写的记忆目录：
```bash
mkdir -p .storage/reviews/ .cache/reviews/
```

### 2. 更新 `.gitignore`
为了保持团队代码库的整洁，请在 `.gitignore` 中加入以下规则：
```gitignore
# 忽略可重建的缓存数据
.cache/

# (可选) 如果你不想和团队共享记忆，也可以忽略 storage
# .storage/
```

### 3. 配置 AI 技能 (Skill Setup)
如果你使用的是支持自定义技能/Agent 的 IDE（如 Trae）：
1. 复制本仓库 [src/system-prompt.md](./src/system-prompt.md) 中的内容，作为该技能的 System Prompt。
2. 为技能勾选 **读写本地文件 (`Read`/`Write`)** 和 **文件检索 (`Glob`/`Grep`)** 的工具权限。
3. (可选) 将 [src/memory-schema.json](./src/memory-schema.json) 作为上下文提供给大模型，确保其严格按照 Schema 生成记忆。

---

## 💬 使用示例 (Usage Examples)

你可以在对话框中通过自然语言直接调用该技能：

**生成复盘：**
> `@dao-genesis 复盘刚才我们修复的 JWT 跨域登录问题`

### 记忆注入工具 (Memory Injector)

除了让大模型生成复盘，你也可以使用提供的 Python CLI 工具，将本地用 Markdown 写的半结构化复盘笔记直接转换为符合 Schema 的 JSON 记录。

**运行脚本：**
```bash
# 转换单个文件
python scripts/inject_memory.py <path_to_markdown>

# 批量转换一个目录下的所有 .md 文件
python scripts/inject_memory.py <path_to_directory>

# 递归批量转换目录及其子目录下的所有 .md 文件
python scripts/inject_memory.py <path_to_directory> -r

# 干跑预览（Dry-Run）：只打印解析生成的 JSON 结果，不写入磁盘
python scripts/inject_memory.py <path_to_markdown_or_directory> --dry-run
```

**Markdown 格式要求：**
使用二级或三级标题（如 `## 关键决策` 或 `### Action Items`）来区分字段，脚本会自动解析并填充到 `.storage/reviews/REV-YYYYMMDD-NNN.json` 中。
缺失的数组字段会自动填充为 `[]`，确保数据始终合法。

---

**查询经验：**
> `@dao-genesis 查询记忆：关于 React Native 列表性能优化的经验`

### 查询演示（遵循 Contract）

用户指令示例：
> `@dao-genesis 查询记忆：schema 扁平化 工具白名单`

内部工具流程（用于调试与对齐 Contract）：
1) Glob：定位候选文件（`.storage/reviews/REV-*.json`）
2) Grep：用关键词初筛命中记录（必要时拆分多个关键词）
3) Read：仅读取少量命中文件片段以提炼“核心结论/行动项”

读取硬阈值：
- 最多读取 3 个文件
- 每个文件最多读取 120 行片段（必要时用 offset/limit）

期望输出（Top N=3，极简返回）：
- `REV-20260417-002` | 核心结论：Schema 扁平化降低写入难度 | 行动：统一工具白名单并补齐极简输出模板

禁止：
- 输出完整 JSON
- 输出整段原文/整份复盘报告

**更新记录：**
> `@dao-genesis 更新记忆 REV-20260417-001，补充一条 Action Item：增加 Redis 缓存层`

**归档记录：**
> `@dao-genesis 归档记忆 REV-20260417-001`

*(注：技能会自动遵循精简输出规范，仅返回被修改字段差异或归档成功提示，严禁输出完整 JSON。)*

### 记忆管理本地脚本 (Memory Manager)

如果需要脱离大模型，通过本地命令行直接修改或归档历史记录，可使用提供的管理脚本。这能确保更新后的数据始终符合 Schema 且不会引入额外字段。

**更新记录：**
```bash
# 覆盖字符串字段（如 task_type, status）
python scripts/manage_memory.py update REV-20260417-001 --field task_type --value "Bug Fix"

# 覆盖数组字段（如 action_items, decisions）
python scripts/manage_memory.py update REV-20260417-001 --field action_items --value "重构鉴权模块"

# 向数组字段追加内容（使用 --append 或 -a）
python scripts/manage_memory.py update REV-20260417-001 --field action_items --value "补充鉴权单元测试" --append
```

**归档记录：**
```bash
python scripts/manage_memory.py archive REV-20260417-001
```

**其他自动化脚本：**
- `scripts/migrate_memory.py`: 用于处理 Schema 升级时的旧数据自动化迁移。
- `scripts/build_memory_cache.py`: 提取活跃复盘记录的摘要并生成检索缓存索引 (`.cache/reviews/search_index.json`)，用于极大降低长周期检索时的 Token 消耗。

---

## 📂 仓库结构 (Repository Structure)

```text
daoAgents/dao-genesis/
├── src/                    # 核心技能资产
│   ├── system-prompt.md    # 技能注入用的大模型 System Prompt
│   └── memory-schema.json  # 记忆数据 JSON Schema 标准
├── docs/                   # 详细文档
│   └── spec.md             # 完整的架构与技术设计说明书
├── CONTRIBUTING.md         # 贡献指南
└── LICENSE                 # 开源协议 (Apache-2.0)
```

---

## 🤝 参与共建 (Contributing)

我们欢迎任何形式的贡献！
你可以提交 PR 来优化 `system-prompt.md` 的逻辑，也可以分享你在使用不同框架时沉淀的**优秀脱敏复盘数据**。

详细规则请阅读 [贡献指南 (CONTRIBUTING.md)](./CONTRIBUTING.md)。

---

## 📄 协议 (License)

本项目采用 [Apache-2.0 License](./LICENSE) 开源。
