# Checklist: 系统性复盘与记忆管理技能创建（GraphQL-Native Edition v3.0）

> **依据文档**: `spec.md` (v3.0, GraphQL-Native Edition, 2026-04-17)
> **规范依据**: GraphQL Specification (June 2018) + GraphQL Relay Specification
> **技术栈要求**:
> - Python 3.14+ 及更高版本
> - FastAPI 框架（与 Python 3.14+ 兼容）
> - PEP 8 编码规范
> - 完整的功能文档、API 接口说明及单元测试用例
> - **TOML 配置文件格式（遵循 PEP 621 规范）**

---

## Phase 1: 概述与设计哲学验证（Overview & Design Philosophy Verification）

### §1.1 背景与动机确认
- [ ] 技能定位明确：**基于图思维（Graph Thinking）** 的结构化复盘与记忆管理机制
- [ ] 核心目标清晰：
  - [ ] 自动提取高价值经验
  - [ ] 沉淀最佳实践
  - [ ] 避免重复错误
  - [ ] 支持团队协作与跨平台同步

### §1.2 设计哲学落地验证（Pure GraphQL & MyST）
- [ ] **六大核心理念全部体现**：

| 理念 | 验证项 | 状态 |
|------|--------|------|
| **一切皆是图** | 复盘记录建模为 GraphQL 图节点（Node），通过 Edge 建立关系 | ☐ |
| **Schema 即契约** | `schema.graphql` 作为唯一的数据契约定义（SDL 格式） | ☐ |
| **按需获取** | 极致 Token 优化策略（Field Selection），仅返回用户请求的核心字段 | ☐ |
| **Query/Mutation 分离** | 四条指令清晰分离读写职责（§5.1 详细定义） | ☐ |
| **强类型验证** | 编译时 + 运行时双重类型检查，所有数据操作经过 GraphQL 类型系统校验 | ☐ |
| **人类可读优先** | 采用 MyST 规范作为主存储格式（`.md` 文件兼顾可读性与可解析性） | ☐ |

### §1.3 变更范围确认（What Changes）
- [ ] **新建组件清单完整**：
  - [ ] `SKILL.md` — 技能主文件（技能定义与 Prompt）
  - [ ] `src/schema.graphql` — GraphQL 强类型 SDL 定义
  - [ ] `tools/md_graphql_converter.py` — MyST MD ↔ GraphQL 双向转换工具
  - [ ] `tools/validate_graphql_schema.py` — GraphQL Schema 合规性校验脚本
  - [ ] `templates/review_template.myst` — 复盘记录标准模板
  - [ ] CI/CD 工作流及相关处理模块
- [ ] **六大核心功能模块已规划**：
  - [ ] 复盘分析引擎（Mutation Operation）
  - [ ] 结构化存储层（Persistent Layer — MyST Markdown 主存储）
  - [ ] 高效检索引擎（Query Operation — 参数化多维度查询）
  - [ ] 记忆管理系统（Mutation Operations — 更新、归档、版本迭代）
  - [ ] Token 优化控制器（Field Selection Philosophy）
  - [ ] 图关系建模器（Graph Relationships — 外部系统追溯链接）

### §1.4 影响范围确认
- [ ] Affected specs：无（全新技能）
- [ ] Affected code：新建技能目录及配套脚本
- [ ] 依赖工具：Glob, Grep, Read, Write（白名单工具集，§5.2 详细定义）
- [ ] 存储路径配置正确：
  - [ ] `.storage/reviews/` — 业务数据存储路径
  - [ ] `.cache/reviews/` — 缓存存储路径

### §1.5 TOML 配置规范验证（PEP 621 Compliance）
- [ ] **TOML 配置文件存在性验证**：
  - [ ] `pyproject.toml` 文件存在于项目根目录
  - [ ] 文件格式符合 TOML 规范（可通过 `toml-validate` 工具校验）
- [ ] **PEP 621 项目元数据验证**：
  - [ ] `[project]` 区块存在且包含必要字段：
    - [ ] `name` — 项目名称
    - [ ] `version` — 版本号（语义化版本）
    - [ ] `requires-python` — Python 版本要求（`>=3.14`）
    - [ ] `description` — 项目描述
  - [ ] `readme` 字段指定 README 文件路径
- [ ] **依赖配置验证**：
  - [ ] `[dependencies]` 区块包含所有运行时依赖
    - [ ] FastAPI 框架依赖已声明
    - [ ] pyyaml 依赖已声明
    - [ ] graphql-core 依赖已声明
    - [ ] python-frontmatter 依赖已声明
  - [ ] `[project.optional-dependencies]` 区块包含开发依赖
    - [ ] `dev` 分组包含 pytest, black, flake8, mypy 等
- [ ] **工具配置验证**：
  - [ ] `[tool.black]` 区块存在，配置代码格式化规则
  - [ ] `[tool.mypy]` 区块存在，配置类型检查规则
  - [ ] `[tool.pytest.ini_options]` 区块存在，配置测试选项
- [ ] **TOML 语法规范验证**：
  - [ ] 所有键名使用小写字母和下划线（snake_case）
  - [ ] 字符串值使用双引号或三引号
  - [ ] 数组和表格语法正确嵌套
  - [ ] 无尾随逗号或非法转义字符
- [ ] **环境变量引用验证**：
  - [ ] 敏感信息使用 `${VAR}` 语法引用环境变量
  - [ ] 无硬编码的 API Key、密码或密钥
- [ ] **禁止项验证**：
  - [ ] ❌ 项目根目录不存在 `requirements.txt`（应使用 `pyproject.toml` 管理依赖）
  - [ ] ❌ 不存在 JSON 格式的配置文件（除非要与特定工具集成）
  - [ ] ❌ 配置项注释未被删除（保留配置意图说明）

---

## Phase 2: 当前局限性与解决方案验证（Limitations & Solutions Verification）

### §2.1 传统 REST/JSON 局限性理解确认
- [ ] 已识别 **6 大核心局限性**并记录应对策略：

| 编号 | 局限类型 | 应对方案 | 状态 |
|-----|---------|---------|------|
| L1 | Over-fetching / Under-fetching | GraphQL Field Selection（按需获取字段） | ☐ |
| L2 | 弱类型约束 | GraphQL SDL 强类型系统 + 编译时+运行时校验 | ☐ |
| L3 | 多端点碎片化 | GraphQL 单端点聚合（所有操作通过单一 Endpoint） | ☐ |
| L4 | 版本控制困难 | Additive Changes 渐进式演进策略（§6.3） | ☐ |
| L5 | 文档同步问题 | GraphQL Introspection 自动生成文档能力 | ☐ |
| L6 | 嵌套查询复杂 | GraphQL 内联 Fragment + Connection Pattern | ☐ |

### §2.2 GraphQL 优势对照表验证
- [ ] **8 大 GraphQL 优势均已在本技能中落地**：

| 编号 | GraphQL 优势 | 落地位置 | 状态 |
|-----|-------------|---------|------|
| A1 | 强类型系统（SDL 完整类型层次） | §3.1 schema.graphql 定义 | ☐ |
| A2 | 按需字段选择（客户端精确指定所需字段） | §6.1 Field Selection Philosophy | ☐ |
| A3 | 单端点聚合（所有操作通过单一 Endpoint） | §5.3 Sequential Resolver Pipeline | ☐ |
| A4 | 内省能力（自动生成文档） | §11.1 Introspection 支持 | ☐ |
| A5 | Query/Mutation 分离（读写操作清晰分离） | §5.1 接口定义 | ☐ |
| A6 | 变量与参数化（强类型 Input Types） | §3.1.5 Input Types 定义 | ☐ |
| A7 | 渐进式演进（Additive Changes 策略） | §6.3 Schema Evolution | ☐ |
| A8 | 订阅支持（实时数据推送，未来扩展） | 预留扩展接口 | ☐ |

- [ ] **核心决策已记录**：采用 **GraphQL SDL 作为类型契约**，MyST Markdown 作为人类可读的主存储，两者通过 `md_graphql_converter.py` 保持同步

---

## Phase 3: 核心功能定义验证（Core Feature Definitions Verification）

### §3.1 GraphQL 强类型数据模型验证（Strongly-Typed Data Model via GraphQL）

#### §3.1.1 自定义标量类型（Custom Scalar Types）
- [ ] `ReviewID` 标量已定义：
  - [ ] 格式约束：`REV-YYYYMMDD-NNN`
  - [ ] 示例值：`REV-20260417-001`
  - [ ] 正则约束：`^REV-[0-9]{8}-[0-9]{3}$`
  - [ ] 使用 `@specifiedBy(url: ...)` directive 声明规范引用
- [ ] `DateTime` 标量已定义：
  - [ ] 格式约束：ISO 8601 日期时间字符串
  - [ ] 示例值：`2026-04-17T08:24:00Z`
  - [ ] 使用 `@specifiedBy(url: "http://tools.ietf.org/html/rfc3339")` directive

#### §3.1.2 枚举类型（Enumeration Types）
- [ ] `ReviewStatus` 枚举已定义且包含以下值：
  - [ ] `ACTIVE` — 活跃状态（默认值），记录可被检索和更新
  - [ ] `ARCHIVED` — 已归档状态，记录仅可读不可修改
  - [ ] 每个枚举值均有详细注释说明用途
- [ ] `TaskType` 枚举已定义且包含以下值：
  - [ ] `FEATURE_IMPLEMENTATION` — 功能实现
  - [ ] `BUG_FIX` — Bug 修复
  - [ ] `REFACTORING` — 代码重构
  - [ ] `ARCHITECTURE_UPGRADE` — 架构升级
  - [ ] `INCIDENT_RESOLUTION` — 故障处理
  - [ ] `TECH_DECISION` — 技术决策
  - [ ] `OTHER` — 其他类型
  - [ ] 每个枚举值均有中文注释

#### §3.1.3 对象类型：Review Node（Object Type）
- [ ] `type Review implements Node` 已正确定义（实现 Node Interface，为 Relay 兼容预留）
- [ ] **Required Fields（标记为 `!` 的非空字段）全部声明**：
  - [ ] `id: ID!` — 全局唯一标识符
  - [ ] `reviewId: ReviewID!` — 业务标识符（使用自定义标量 ReviewID）
  - [ ] `timestamp: DateTime!` — 创建时间戳（ISO 8601 格式）
  - [ ] `participants: [String!]!` — 参与者列表（至少包含一个参与者）
  - [ ] `taskType: TaskType!` — 任务类型枚举
  - [ ] `decisions: [String!]!` — 关键决策列表
  - [ ] `successFactors: [String!]!` — 成功因素列表
  - [ ] `failureReasons: [String!]!` — 失败原因列表
  - [ ] `bestPractices: [String!]!` — 最佳实践列表
  - [ ] `actionItems: [String!]!` — 行动项列表
  - [ ] `status: ReviewStatus!` — 当前状态（默认 ACTIVE）
- [ ] **Optional Fields 全部声明**：
  - [ ] `schemaVersion: String` — Schema 版本号（默认 `"1.2"`）
  - [ ] `issueUrl: String` — 关联 Issue URL（向上追溯 Edge）
  - [ ] `prUrl: String` — 关联 PR/MR URL（向上追溯 Edge）
  - [ ] `projectId: String` — 项目标识
  - [ ] `tags: [String!]` — 标签列表
  - [ ] `coreConclusion: String` — 核心结论摘要（≤150 字符）
- [ ] 字段命名遵循 **camelCase** 规范（GraphQL 官方推荐）
- [ ] 每个字段均有详细注释说明（支持 Introspection 自动生成文档）

#### §3.1.4 接口类型：Node Interface
- [ ] `interface Node` 已定义：
  - [ ] 包含唯一字段 `id: ID!`
  - [ ] 符合 GraphQL Relay 规范的全局节点接口定义
  - [ ] 注释说明其为所有实体的统一访问入口

#### §3.1.5 输入类型（Input Types）
- [ ] `CreateReviewInput` 已定义（用于 createReview Mutation 参数）：
  - [ ] **Required Fields**：`participants`, `taskType`, `decisions`, `successFactors`, `failureReasons`, `bestPractices`, `actionItems`（均为非空数组或枚举）
  - [ ] **Optional Fields**：`issueUrl`, `prUrl`, `projectId`, `tags`
  - [ ] 每个字段均有注释说明用途
- [ ] `UpdateReviewInput` 已定义（用于 updateReview Mutation 参数，采用 Partial Update Pattern）：
  - [ ] **必填字段**：`reviewId: ReviewID!`
  - [ ] **数组追加字段（Append）**：
    - [ ] `decisionsAppend: [String]`
    - [ ] `successFactorsAppend: [String]`
    - [ ] `failureReasonsAppend: [String]`
    - [ ] `bestPracticesAppend: [String]`
    - [ ] `actionItemsAppend: [String]`
  - [ ] **字符串覆写字段（Override）**：
    - [ ] `taskTypeOverride: TaskType`
    - [ ] `statusOverride: ReviewStatus`
    - [ ] `issueUrlOverride: String`
    - [ ] `prUrlOverride: String`

#### §3.1.6 查询与变更根类型（Root Types）
- [ ] `type Query`（查询根类型）已定义：
  - [ ] `reviews()` 字段：
    - [ ] 支持参数：`keywords: [String]`, `taskType: TaskType`, `status: ReviewStatus = ACTIVE`, `dateFrom: DateTime`, `dateTo: DateTime`, `projectId: String`, `limit: Int = 3`
    - [ ] 返回类型：`[Review!]!`
    - [ ] Hard Limit: limit 最大值为 3
  - [ ] `review(id: ReviewID!)` 字段：根据 ID 获取单个复盘记录，返回 `Review`
  - [ ] `node(id: ID!)` 字段：GraphQL Relay 兼容的节点查询，返回 `Node`
- [ ] `type Mutation`（变更根类型）已定义：
  - [ ] `createReview(input: CreateReviewInput!)` → 返回 `CreateReviewPayload!`
  - [ ] `updateReview(input: UpdateReviewInput!)` → 返回 `UpdateReviewPayload!`
  - [ ] `archiveReview(reviewId: ReviewID!)` → 返回 `ArchiveReviewPayload!`

#### §3.1.7 Payload 类型（Mutation Payload Pattern）
- [ ] `CreateReviewPayload` 已定义：
  - [ ] `review: Review` — 新创建的复盘记录节点
  - [ ] `clientMutationId: String` — 用于乐观更新
- [ ] `UpdateReviewPayload` 已定义：
  - [ ] `review: Review` — 更新后的复盘记录节点
  - [ ] `changeSummary: String` — 变更摘要信息
  - [ ] `clientMutationId: String`
- [ ] `ArchiveReviewPayload` 已定义：
  - [ ] `review: Review` — 归档后的节点（status = ARCHIVED）
  - [ ] `previousStatus: ReviewStatus` — 归档前的状态值
  - [ ] `clientMutationId: String`
- [ ] 设计说明确认：采用 **Mutation Payload Pattern**（而非直接返回对象），为未来错误信息和扩展字段预留空间

#### Scenario: GraphQL Schema 合规性校验验证
- [ ] **Phase 1: 编译时验证（Compile-Time Validation）** 已实现：
  - [ ] Type Check：所有输入参数的类型必须匹配 Input Type 定义
    - [ ] `reviewId` 匹配 `ReviewID` 标量的正则约束 `^REV-[0-9]{8}-[0-9]{3}$`
    - [ ] `timestamp` 符合 `DateTime` 标量的 ISO 8601 格式
    - [ ] `taskType` 是 `TaskType` 枚举的有效值
    - [ ] `status` 是 `ReviewStatus` 枚举的有效值（`ACTIVE` / `ARCHIVED`）
  - [ ] Non-Null Constraint：所有标记为 `!` 的字段必须提供且非空
  - [ ] List Non-Null：`[String!]!` 表示列表本身非空且元素非空（允许空列表 `[]`，禁止 `null`）
- [ ] **Phase 2: 运行时验证（Runtime Validation）** 已实现：
  - [ ] Field Validation Rules：应用自定义验证规则（通过 `@constraint` directive 或 resolver 逻辑）
  - [ ] Business Logic Checks：执行业务规则校验（如唯一性、引用完整性）

#### Scenario: 向后兼容的 Schema 演进验证
- [ ] **允许的操作（Allowed Changes）**：
  - [ ] ✅ 新增字段（Additive Change）：如 `tags: [String!]`, `coreConclusion: String`
  - [ ] 新增可选 Arguments
  - [ ] 使用 `@deprecated` 废弃旧字段
  - [ ] 新增 Enum Values（谨慎使用）
- [ ] **禁止的操作（Forbidden Changes）**：
  - [ ] ❌ 删除或重名字段（Breaking Change）
  - [ ] ❌ 改变 Required Field 的类型或语义
  - [ ] ❌ 移除 Enum Values
- [ ] **演进策略四原则**已落实：
  - [ ] Additive Changes Only：仅允许新增字段
  - [ ] Default Values for New Fields：新字段必须提供合理默认值
  - [ ] @deprecated Directive：废弃旧字段时使用 `@deprecated(reason: "...")`
  - [ ] Schema Stitching/Merging：多版本 Schema 合并工具支持

### §3.2 复盘分析能力验证（Review Analysis Engine）
- [ ] 引擎作为**业务逻辑层（Business Logic Layer）**的核心组件
- [ ] **四维解析模型全部实现**：

| 维度 | 名称 | 功能描述 | 状态 |
|-----|------|---------|------|
| 1 | **背景溯源** | 识别任务意图 → 提取痛点 → 确定验收标准 | ☐ |
| 2 | **决策链路树** | 识别技术选型 → 梳理权衡考量 → 记录否决方案 | ☐ |
| 3 | **红黑榜总结** | 提炼成功因素（红榜）→ 识别失败教训（黑榜）→ 根因分析 | ☐ |
| 4 | **复用价值判定** | 评估通用性 → 筛选 SOP → 标记场景标签 | ☐ |

#### Scenario: 执行完整复盘（GraphQL Mutation 流程）验证
- [ ] **Phase 1: 输入解析与验证**：
  - [ ] 解析自然语言输入，提取结构化信息
  - [ ] 验证必要参数完整性（participants 或 context 至少一项非空）
  - [ ] 缺少关键信息时使用 AskUserQuestion 补充（而非静默猜测）
- [ ] **Phase 2: 分析引擎执行**：
  - [ ] 应用多维解析模型生成中间结果
  - [ ] 构建 **GraphQL Variable 对象**
- [ ] **Phase 3: GraphQL Schema 映射与序列化**：
  - [ ] 将中间结果映射到 `CreateReviewInput` 类型（填充所有 Required Fields）
  - [ ] 生成唯一 `reviewId`（格式：`REV-YYYYMMDD-NNN`，NNN 为当日递增序号）
  - [ ] 设置 `timestamp` 为当前 ISO 8601 时间
  - [ ] 设置默认值：`status=ACTIVE`, `schemaVersion="1.2"`
- [ ] **Phase 4: 执行 Mutation 与持久化**：
  - [ ] 执行 `createReview` Mutation（使用标准 Payload Pattern）
  - [ ] 写入 MyST Markdown 文件至 `.storage/reviews/REV-20260417-001.md`
  - [ ] **返回极简结果**（遵循 Field Selection Philosophy）：
    - [ ] MUST: 返回 `reviewId`（如 `REV-20260417-001`）
    - [ ] OPTIONAL: 1 行 file path + 1-2 行核心 actionItems 摘要
    - [ ] FORBIDDEN: 完整对象展开 / 超过 10 行详情 / 指令复述

#### Scenario: 极简输出契约（Field Selection Philosophy）验证
- [ ] **输出规则严格执行**：

| 规则类型 | 约束内容 | 类比 GraphQL | 状态 |
|---------|---------|-------------|------|
| MUST | 返回 `reviewId`（如 `REV-20260417-001`） | 选择 `reviewId` 字段 | ☐ |
| OPTIONAL | 1 行 file path + 1-2 行核心 actionItems 摘要 | 选择 `coreConclusion` 字段 | ☐ |
| FORBIDDEN | 完整对象展开 / 超过 10 行详情 / 指令复述 | 禁止 `{ review { ... on Review { * } } }` | ☐ |

### §3.3 记忆检索能力验证（Memory Query & Retrieval）
- [ ] 提供**参数化的高效多维度记忆检索功能**
- [ ] 完全基于 **GraphQL Query Language**

#### §3.3.1 查询参数模型
- [ ] 参考 `Query.reviews` 字段的 Arguments 定义已实现
- [ ] 支持参数：keywords, taskType, status(默认 ACTIVE), dateFrom, dateTo, projectId, limit(默认 3, Hard Limit)

#### §3.3.2 三阶段检索管道（Resolver Pipeline）
- [ ] **Phase 1: 候选集生成**：
  - [ ] 使用 `Glob(".storage/reviews/REV-*.md")` 定位候选文件
  - [ ] 类比 GraphQL DataLoader batching
- [ ] **Phase 2: 关键词初筛**：
  - [ ] 使用 `Grep(keywords[])` 多关键词 OR 逻辑过滤
  - [ ] 类比 GraphQL @filter directive
- [ ] **Phase 3: 精准读取排序**：
  - [ ] 使用 `Read(top 3, max 120 lines)` 提取内容
  - [ ] 类比 GraphQL Resolver Execution with Pagination
- [ ] **相关度评分因子**（按优先级排序）：
  - [ ] 关键词命中数量（主要因子）
  - [ ] 时间新鲜度（可选加权）
  - [ ] `status=ACTIVE` 优先于 `ARCHIVED`

#### Scenario: 执行多条件参数化查询验证
- [ ] **Step 1: 参数解析与构建**：
  - [ ] 正确构建 GraphQL Query（含 Variables）
  - [ ] keywords, dateFrom, limit 等参数映射正确
- [ ] **Step 2: 执行三阶段检索管道**：
  - [ ] Glob → Grep → Read 流程完整执行
- [ ] **Step 3: 格式化返回结果**（Fragment 格式，Top 3）：
  - [ ] 格式：`[REV-ID] | 核心结论：{内容} | 行动：{actionItem}`
  - [ ] 包含命中总数提示

#### Scenario: 查询阈值溢出处理验证
- [ ] 当候选文件数 > 3 或单文件行数 > 120 时：
  - [ ] 返回 ⚠️ 提示消息（含命中总数和建议缩小范围的具体示例）
  - [ ] 示例：`@skill 查询记忆：支付 超时 近一个月`

### §3.4 记忆更新与归档能力验证（Memory Maintenance）
- [ ] 提供**原子化更新**与**软删除归档**功能
- [ ] 完全基于 **GraphQL Mutation Language**

#### §3.4.1 更新操作语义（Partial Update Pattern）
- [ ] **三种操作模式均已实现**：

| 操作类型 | 适用字段 | GraphQL 操作 | 示例 | 状态 |
|---------|---------|-------------|------|------|
| **数组追加** | decisions, successFactors, failureReasons, bestPractices, actionItems | `xxxAppend: [String]` | `actionItemsAppend: ["补充回调压测基线"]` | ☐ |
| **字符串覆写** | taskType, status, issueUrl, prUrl, projectId | `xxxOverride: Type` | `statusOverride: ARCHIVED` | ☐ |
| **完整替换** | 全量更新（谨慎使用） | 提供完整 `UpdateReviewInput` | 需提供所有字段 | ☐ |

#### Scenario: 执行字段级更新验证
- [ ] 正确构建 `updateReview` Mutation
- [ ] Variables 中 reviewId 和追加字段映射正确
- [ ] **返回极简 Diff 结果**：
  - [ ] 格式：`✅ REV-20260417-001 已更新` + `📝 变更：actionItems: [新增] 补充回调压测基线`

#### Scenario: 执行归档操作验证
- [ ] 正确构建 `archiveReview` Mutation
- [ ] 返回格式：`✅ [REV-20260417-001] 归档成功（状态：ACTIVE → ARCHIVED）`
- [ ] Payload 包含 previousStatus 字段（显示归档前状态为 ACTIVE）

#### Scenario: 并发冲突检测验证
- [ ] 检测到并发编辑迹象（Git 冲突标记等）时：
  - [ ] 返回 GraphQL 错误格式（符合 Error Extensions 规范）
  - [ ] 错误码：`E_WRITE_CONFLICT`
  - [ ] extensions.code: `WRITE_CONFLICT`
  - [ ] extensions.hint: 可操作的解决建议
  - [ ] extensions.reviewId: 冲突记录 ID

### §3.5 图关系建模与追溯能力验证（Graph Relationships）
- [ ] 支持**原生 GraphQL 图思维的数据建模**
- [ ] 实现与外部系统的双向追溯

#### 关系边定义（Edge Definitions）验证
- [ ] **向上追溯边**：
  - [ ] `issueUrl: String` — 关联 Issue/Bug Report
  - [ ] URL Pattern 支持：GitHub/GitLab/AtomGit Issues URL
  - [ ] `prUrl: String` — 关联 PR/MR
  - [ ] URL Pattern 支持：GitHub/GitLab/AtomGit Pull/Merge URL
- [ ] **向下穿透边**：
  - [ ] 自动 Comment 回写机制（通过 Issue Tracker API）
  - [ ] 复盘结论回写到 Issue/PR

#### Scenario: 双向追溯演示验证
- [ ] **向上追溯**（从记忆到代码现场）：
  - [ ] 通过 `review(id:)` Query 获取 issueUrl 和 prUrl
  - [ ] URL 可点击跳转到对应页面
- [ ] **向下穿透**（从现场到结论）：
  - [ ] 通过 Issue Tracker API 自动添加评论
  - [ ] 评论包含 reviewId + 核心结论
  - [ ] 开发者可在 Issue 页面直接看到复盘结论

### §3.6 GraphQL Schema 映射层架构验证（Schema Mapping Layer）
- [ ] 映射层作为 MyST Markdown 与 GraphQL 类型系统之间的**转换与验证中间层**

#### §3.6.1 映射层的职责边界
- [ ] **四大职责均已实现**：

| 职责 | 说明 | 实现组件 | 状态 |
|------|------|---------|------|
| **类型映射** | MyST Front Matter (snake_case) ↔ GraphQL Type (camelCase) 双向映射 | `md_graphql_converter.py` | ☐ |
| **结构验证** | 校验 MyST 文件是否符合 GraphQL Schema 定义的约束 | `validate_graphql_schema.py` | ☐ |
| **字段解析** | GraphQL Query Arguments → MyST 文件检索条件 | Resolver Pipeline (Glob/Grep/Read) | ☐ |
| **序列化输出** | MyST 内容 → GraphQL Response Field Selection | Formatter | ☐ |

#### §3.6.2 MyST ↔ GraphQL 字段映射规则
- [ ] **映射表完整且准确**：

| MyST Front Matter (snake_case) | GraphQL Field (camelCase) | GraphQL 类型 | 状态 |
|-------------------------------|---------------------------|-------------|------|
| `review_id` | `reviewId` | `ReviewID!` | ☐ |
| `timestamp` | `timestamp` | `DateTime!` | ☐ |
| `task_type` | `taskType` | `TaskType!` | ☐ |
| `status` | `status` | `ReviewStatus!` | ☐ |
| `decisions` (admonition content) | `decisions` | `[String!]!` | ☐ |
| `success_factors` (admonition content) | `successFactors` | `[String!]!` | ☐ |
| `failure_reasons` (admonition content) | `failureReasons` | `[String!]!` | ☐ |
| `best_practices` (admonition content) | `bestPractices` | `[String!]!` | ☐ |
| `action_items` (admonition content) | `actionItems` | `[String!]!` | ☐ |
| `core_conclusion` | `coreConclusion` | `String` (≤150 字符) | ☐ |
| `pr_url` | `prUrl` | `String` | ☐ |
| `issue_url` | `issueUrl` | `String` | ☐ |

#### §3.6.3 查询到检索的映射流程验证
- [ ] 用户指令 → 指令解析层 → GraphQL Query 构建 → Resolver Pipeline → Field Selection → 格式化输出
- [ ] 各阶段职责清晰，数据流无丢失

#### §3.6.4 写入到持久化的映射流程验证
- [ ] 用户指令 → 复盘分析引擎 → GraphQL Mutation → Resolver 执行 → 转换工具校验 → 极简返回
- [ ] reviewId 生成、timestamp 设置、默认值赋值逻辑正确

#### §3.6.5 映射层与 Resolver 的区别确认
- [ ] 映射层负责 MyST ↔ GraphQL 之间的格式转换与验证
- [ ] Resolver 层负责 GraphQL Query/Mutation ↔ 实际数据的读写逻辑执行
- [ ] 两层职责边界清晰，不互相越界

---

## Phase 4: 数据模型与存储架构验证（Data Model & Storage Architecture Verification）

### §4.1 MyST Markdown 主存储格式验证
- [ ] **文件命名规范正确**：
  - [ ] 格式：`.storage/reviews/REV-{YYYYMMDD}-{NNN}.md`
  - [ ] 示例：`.storage/reviews/REV-20260417-001.md`
- [ ] **重要变更确认**：
  - [ ] ✅ 已移除辅助 `.json` 文件
  - [ ] ✅ `schema.graphql` 是唯一的数据契约定义
  - [ ] ✅ MyST Markdown 是人类可读的主存储格式
  - [ ] ✅ 两者通过 `md_graphql_converter.py` 保持同步

#### §4.1.2 完整模板示例验证（MyST ↔ GraphQL 映射）
- [ ] `templates/review_template.myst` 存在且格式正确
- [ ] **YAML Front Matter 完整性**：
  - [ ] 以 `---` delimiter 开始和结束
  - [ ] 所有 Required Fields（10 个）均存在且非空
  - [ ] Optional Fields（schema_version, pr_url, issue_url, project_id, tags, core_conclusion）齐全
  - [ ] snake_case 命名规范一致
  - [ ] review_id 占位符格式匹配 ReviewID 正则
  - [ ] timestamp 占位符为 ISO 8601 格式
- [ ] **Markdown 正文结构**：
  - [ ] 标题行格式标准：`# 复盘报告：PR #XXX - {描述}`
  - [ ] 元信息行存在（创建时间、参与者、状态）
- [ ] **Admonition Directives 完整性（5 个必需区块）**：
  - [ ] ⚙️ 关键决策点 (Key Decisions) — `class: decision` — 对应 `decisions: [String!]!`
  - [ ] ✅ 成功因素 (Success Factors) — `class: success` — 对应 `successFactors: [String!]!`
  - [ ] ❌ 问题与教训 (Issues & Lessons) — `class: warning` — 对应 `failureReasons: [String!]!`
  - [ ] 💡 最佳实践 (Best Practices) — `class: tip` — 对应 `bestPractices: [String!]!`
  - [ ] 📋 行动项 (Action Items) — `class: important` — 对应 `actionItems: [String!]!`
  - [ ] 每个 admonition 的 class 属性值正确
  - [ ] 每个 admonition 内容区域非空
  - [ ] 支持 `:collapse: true` 属性（decision 区块）
- [ ] **核心结论段落**：
  - [ ] 位于文件末尾，以分隔线后开始
  - [ ] 格式：`**🎯 核心结论**：{内容}`
  - [ ] 内容长度 ≤150 字符

### §4.2 MyST Directive 到 GraphQL 字段的映射关系验证
- [ ] **Directive 映射表完整**：

| MyST Directive 名称 | CSS Class | GraphQL 字段名 | GraphQL 类型 | 状态 |
|---------------|----------|---------------|-------------|------|
| `{admonition} decision` | `.decision-block` | `decisions` | `[String!]!` | ☐ |
| `{admonition} success` | `.success-factor` | `successFactors` | `[String!]!` | ☐ |
| `{admonition} warning` | `.failure-reason` | `failureReasons` | `[String!]!` | ☐ |
| `{admonition} tip` | `.best-practice` | `bestPractices` | `[String!]!` | ☐ |
| `{admonition} important` | `.action-item` | `actionItems` | `[String!]!` | ☐ |

### §4.3 双格式协同架构验证（MyST Primary + GraphQL Schema Mapping）
- [ ] **角色分工明确**：

| 维度 | 主格式 (.md) | GraphQL Schema (.graphql) | 状态 |
|-----|-------------|--------------------------|------|
| **角色** | 人类可读的主存储 | 类型契约定义与校验层 | ☐ |
| **用途** | 人工阅读、Git 版本控制、IDE 预览 | 类型安全校验、程序化验证、Introspection | ☐ |
| **生成方式** | 手动或 LLM 生成 | 手动编写（SDL 格式） | ☐ |
| **编辑权限** | ✅ 可手动编辑 | ⚠️ 仅限 Schema 演进时修改 | ☐ |
| **同步机制** | 写入后通过 converter 验证合规性 | Schema 变更后需重新验证所有 .md 文件 | ☐ |
| **验证方式** | `validate_graphql_schema.py --check-md` | `graphql validate` 或 `graphqxl` | ☐ |

- [ ] **架构决策已记录**：
  - [ ] 主存储：MyST Markdown（人类友好，便于 Git 版本控制和 IDE 直接阅读）
  - [ ] 类型契约：GraphQL SDL（机器可读的类型定义，作为验证规则）
  - [ ] 映射关系：`md_graphql_converter.py` 负责 MyST → GraphQL 的双向验证
  - [ ] 数据流：MyST 是事实存储（Source of Truth），GraphQL Schema 是校验规则（Validation Contract）

### §4.4 GraphQL Schema 合规性校验要求验证
- [ ] **9 项检查项全部实现**：

| 检查项 | 要求 | 校验命令 | 状态 |
|-------|------|---------|------|
| YAML Front Matter 完整性 | 必须包含所有 Required Fields | `--check-frontmatter` | ☐ |
| Directive 规范性 | 必须使用预定义 class（decision/success/warning/tip/important） | `--check-directives` | ☐ |
| 核心结论存在性 | 文件末尾必须包含 `🎯 核心结论`（≤150 字符） | `--check-conclusion` | ☐ |
| Markdown 语法正确性 | 无损坏链接、错误嵌套、非法转义字符 | `--check-syntax` 或 markdownlint | ☐ |
| 文件编码一致性 | UTF-8 编码，LF 行尾符 | file -i 或 Git hooks | ☐ |
| GraphQL 类型映射正确性 | 每个 Front Matter 字段必须对应合法字段 | `--check-mapping` | ☐ |
| Enum 值有效性 | task_type、status 在预定义范围内 | `--check-enums` | ☐ |
| Scalar 格式合规性 | review_id 匹配 ReviewID 正则，timestamp 符合 ISO 8601 | `--check-scalars` | ☐ |

---

## Phase 5: 接口规范与操作流程验证（Interface Specifications & Operations Verification）

### §5.0 SKILL.md 指令解析层验证（Instruction Parsing Layer）
- [ ] SKILL.md 作为技能的 Prompt 定义，负责将用户自然语言指令解析为 GraphQL 操作

#### §5.0.1 指令到 GraphQL 的映射架构验证
- [ ] 数据流完整：用户指令 → Prompt 解析 → GraphQL Operation 映射 → 参数提取 → Resolver Pipeline → Field Selection 输出

#### §5.0.2 指令类型识别规则验证
- [ ] **四种指令类型识别规则完整**：

| 用户指令关键词 | GraphQL 操作 | 触发条件 | 状态 |
|--------------|-------------|---------|------|
| `复盘`、`总结`、`review` | `createReview` | 包含上下文描述的创建请求 | ☐ |
| `查询记忆`、`搜索记忆`、`检索` | `reviews` / `review` | 包含查询条件（关键词/时间/类型） | ☐ |
| `更新记忆`、`修改记忆`、`补充` | `updateReview` | 包含 reviewId + 修改内容 | ☐ |
| `归档记忆`、`删除记忆` | `archiveReview` | 包含 reviewId + 归档意图 | ☐ |

#### §5.0.3 指令参数提取规范验证
- [ ] **参数提取规则完整**：

| 参数类型 | 提取来源 | GraphQL Variable | 状态 |
|---------|---------|----------------|------|
| `reviewId` | 指令中的 `REV-YYYYMMDD-NNN` 格式 | `$reviewId: ReviewID!` | ☐ |
| `keywords` | 指令中的自然语言关键词 | `$keywords: [String]` | ☐ |
| `taskType` | 从上下文推断或显式指定 | `$taskType: TaskType` | ☐ |
| `dateFrom/dateTo` | 时间表达式（"近三个月"→ ISO 8601） | `$dateFrom: DateTime`, `$dateTo: DateTime` | ☐ |
| `status` | 默认 `ACTIVE`，或显式指定 `ARCHIVED` | `$status: ReviewStatus = ACTIVE` | ☐ |
| `actionItemsAppend` | 追加的行动项内容 | `$actionItemsAppend: [String]` | ☐ |

#### §5.0.4 SKILL.md 与 GraphQL Schema 的集成验证
- [ ] 指令解析：用户指令 → GraphQL Variables
- [ ] Schema 校验：通过 `schema.graphql` 验证参数类型
- [ ] 类型安全：所有输入经过 GraphQL Input Type 校验
- [ ] 设计说明确认：SKILL.md 不直接返回完整 Query/Mutation 字符串，而是通过 Prompt 引导 LLM 生成符合 Schema 约束的操作

### §5.1 接口定义验证（GraphQL Query/Mutation 分离模式）
- [ ] **Mutation Operations（写操作）定义完整**：

| 指令 | 触发方式 | 功能 | 对应 GraphQL Mutation | 状态 |
|-----|---------|------|---------------------|------|
| `@skill 复盘 [上下文]` | 用户主动触发 | 执行系统性复盘并保存 | `createReview` | ☐ |
| `@skill 更新记忆 [id] [修改]` | 用户主动触发 | 更新指定记录 | `updateReview` | ☐ |
| `@skill 归档记忆 [id]` | 用户主动触发 | 归档过时记录 | `archiveReview` | ☐ |

- [ ] **Query Operations（读操作）定义完整**：

| 指令 | 触发方式 | 功能 | 对应 GraphQL Query | 状态 |
|-----|---------|------|------------------|------|
| `@skill 查询记忆 [条件]` | 用户主动触发 | 检索历史复盘记录 | `reviews` / `review` | ☐ |

### §5.2 工具白名单验证（Whitelist Policy）
- [ ] **白名单工具集严格限制**：

| 工具名称 | 用途 | 类比 GraphQL 概念 | 状态 |
|---------|------|------------------|------|
| `Glob` | 文件名模式匹配定位候选集 | Schema Introspection + DataLoader | ☐ |
| `Grep` | 文件内容关键词搜索初筛 | @filter / @search Directive | ☐ |
| `Read` | 读取文件内容（必须使用 offset/limit） | Resolver Execution（with Pagination） | ☐ |
| `Write` | 写入/覆盖文件内容 | Mutation Resolver Execution | ☐ |

- [ ] **禁止项严格执行**：
  - [ ] ❌ 任何 Shell 命令（RunCommand 等）
  - [ ] ❌ 任何未在白名单中的工具
  - [ ] ❌ 文件系统遍历（LS 大目录列举）

### §5.3 GraphQL 操作流程验证（Sequential Resolver Pipeline）
- [ ] **六步 Pipeline 完整执行**：
  - [ ] Step 1: **解析（Parse）**：接收自然语言指令 → 构建 GraphQL AST
  - [ ] Step 2: **验证（Validate）**：AST 通过 GraphQL Schema Validation
  - [ ] Step 3: **定位（Locate）**：Glob/Grep 快速定位目标文件绝对路径（DataLoader batching）
  - [ ] Step 4: **执行（Execute）**：针对性读取具体内容（大文件必须使用 offset/limit，类比 Cursor-based Pagination）
  - [ ] Step 5: **持久化（Persist）**：整理完整内容后 Write 覆盖写回（严禁 Shell 操作）
  - [ ] Step 6: **返回（Return）**：按照 Query 的 Field Set 精确返回结果（Field Selection）

---

## Phase 6: 约束控制与质量保障验证（Constraints & Quality Assurance Verification）

### §6.1 Token 优化控制验证（Field Selection Philosophy）

#### §6.1.1 输入侧优化（Variable Parsing）
- [ ] **分段读取**：使用 offset/limit 参数分页读取（类比 Connection / Cursor-based Pagination）
- [ ] **信息过滤**：丢弃低价值上下文（日志堆栈、无关闲聊、未修改代码）（类比 @skip / @include Directives）

#### §6.1.2 存储侧优化（Schema Design Best Practices）
- [ ] **扁平化结构**：`tags: ["react", "frontend"]`（对应 GraphQL `[String!]`），避免过度嵌套
- [ ] **信息提纯**：精炼的 Scalar 值（如 `"所有对外服务调用必须设置超时和重试"`），避免冗长自由文本
- [ ] **类型安全**：使用枚举约束（如 `taskType: TaskType!`），避免无类型约束的自由字符串

#### §6.1.3 输出侧优化（Response Shape Control）
- [ ] **查询场景（Query Response）**：
  - [ ] 限制返回数量：Top N=3（通过 `limit: Int = 3` Argument 控制）
  - [ ] Fragment 格式：`[reviewId] | 核心结论：{coreConclusion} | 行动：{actionItems[0]}`
  - [ ] FORBIDDEN：完整 Object 展开 / 整段原文 / 未请求字段
- [ ] **变更场景（Mutation Response）**：
  - [ ] 仅返回 Payload 中的关键字段：`{ review { reviewId status }, changeSummary }`
  - [ ] FORBIDDEN：完整文件内容 / 未变更字段
- [ ] **通用禁令严格执行**：
  - [ ] ❌ 禁止复述用户指令
  - [ ] ❌ 禁止过渡性语句（"我帮您查询了..."、"以下是..."）
  - [ ] ❌ 禁止礼貌性废话

#### §6.1.4 读取硬阈值（Pagination Limits）
- [ ] **最大返回节点数**：3 个 Review（类比 `first: Int = 3` in Connection）
  - [ ] 超出行为：要求用户缩小查询条件
- [ ] **每节点最大行数**：120 行（Custom Scalar limit）
  - [ ] 超出行为：要求用户提供更精确条件

### §6.2 错误处理机制验证（Predictable Error Contract via GraphQL Errors）

#### §6.2.1 错误码体系（GraphQL Error Extensions）
- [ ] **五大错误码完整覆盖**：

| 错误码 | HTTP 类比 | GraphQL Error Code | 场景描述 | 状态 |
|-------|----------|-------------------|---------|------|
| `E_CMD_INVALID` | 400 Bad Request | `BAD_USER_INPUT` | 指令无法解析或缺少必要参数 | ☐ |
| `E_STORAGE_UNAVAILABLE` | 503 Service Unavailable | `INTERNAL_SERVER_ERROR` | 存储目录不存在或无权限访问 | ☐ |
| `E_NOT_FOUND` | 404 Not Found | `NOT_FOUND` | 查询或更新的 reviewId 不存在 | ☐ |
| `E_SCHEMA_MISMATCH` | 422 Unprocessable Entity | `GRAPHQL_VALIDATION_FAILED` | 结构损坏或 Schema 版本不兼容 | ☐ |
| `E_WRITE_CONFLICT` | 409 Conflict | `CONFLICT` | 写入冲突或并发编辑 | ☐ |

#### §6.2.2 标准 GraphQL 错误格式验证
- [ ] 错误响应符合 GraphQL Spec 标准：
  - [ ] 包含 `errors` 数组
  - [ ] 每个 error 包含 `message`（格式：`E_CODE | {摘要}`）
  - [ ] 每个 error 包含 `locations`（行号和列号）
  - [ ] 每个 error 包含 `path`（字段路径）
  - [ ] 每个 error 包含 `extensions`：
    - [ ] `code`: GraphQL Error Code
    - [ ] `hint`: 可操作的修复建议
- [ ] **错误响应示例集合已测试**：
  - [ ] Example 1: E_CMD_INVALID 格式正确
  - [ ] Example 2: E_SCHEMA_MISMATCH 格式正确（含迁移脚本建议）

### §6.3 向后兼容性与演进策略验证（Schema Evolution）
- [ ] **API 稳定性原则**：

| 允许（Allowed） | 禁止（Forbidden） | 状态 |
|----------------|------------------|------|
| ✅ 新增字段（Additive Changes） | ❌ 删除或重名字段（Breaking Change） | ☐ |
| ✅ 新增可选 Arguments | ❌ 改变 Required Field 的类型或语义 | ☐ |
| ✅ 使用 `@deprecated` 废弃旧字段 | ❌ 修改输出类型的核心结构 | ☐ |
| ✅ 新增 Enum Values（谨慎使用） | ❌ 移除 Enum Values | ☐ |

- [ ] **弃用策略（@deprecated Directive）三阶段渐进弃用**：

| 阶段 | 版本 | 行为 | GraphQL 机制 | 状态 |
|-----|------|------|-------------|------|
| T-N | 当前版本 | 标记为 `@deprecated`，但仍可查询 | `@deprecated(reason: "...")` | ☐ |
| T-N+1 | 下一版本 | 强烈建议迁移到替代方案，文档高亮警告 | Introspection `isDeprecated: true` | ☐ |
| T-N+2 | 后续版本 | 移除字段，查询该字段返回 `null` | Schema 清理 | ☐ |

### §6.4 跨平台与协作支持验证
- [ ] **存储格式**：MyST Markdown（纯文本）+ GraphQL SDL（跨操作系统兼容）
- [ ] **路径规范**：严禁 OS 绝对路径，仅使用相对路径或模块路径
- [ ] **Git 协作**：`.storage/` 纳入版本控制，`.cache/` 加入 `.gitignore`
- [ ] **全局记忆**：可选配置 `~/.trae/global_storage/` 用于跨项目通用经验
- [ ] **Schema 共享**：`schema.graphql` 可发布至 GraphQL Registry 或 Git Submodule

---

## Phase 7: CI/CD 集成验证（Automated Closed-Loop & CI/CD Integration Verification）

### §7.1 架构总览验证
- [ ] **CI/CD 流水线架构图逻辑正确**：
  - [ ] PR/MR Merged to Main → Trigger GitHub Actions Workflow
  - [ ] → Data Collection (GitHub/GitLab/AtomGit API)
  - [ ] → Code Review + Diff → Data Aggregation Module
  - [ ] → LLM Processing + GraphQL Mapping → Structured Report (MyST + GraphQL)
  - [ ] → .storage/reviews/ 存储
  - [ ] → Issue Writeback (Issue Tracker API)
  - [ ] → Comment with reviewId → Original Issue
  - [ ] → Traceability Link 双向关联

### §7.2 组件 1: GitHub Actions 工作流验证
- [ ] **触发器配置正确**：
  - [ ] `pull_request.types: [closed]` + `branches: [main, master]`
  - [ ] `merge_request.type: merged` + `target_branch: [main, master]`
  - [ ] YAML 语法正确（可通过 `act` 本地测试）
- [ ] **优先级处理规则实现**：

| 优先级 | Label 条件 | 执行时机 | Review Mode | Issue 回写 | 状态 |
|-------|-----------|---------|-------------|-----------|------|
| 🔴 高 | `bug`, `architecture` | 立即 | Full Review Mode | ✅ 强制 | ☐ |
| 🟡 中 | `feature`, `refactor`, `hotfix` | 延迟 5 分钟 | Standard Review Mode | 可选 | ☐ |
| 🟢 低 | 其他类型 | 每小时批量 | Summary Only Mode | ❌ 不回写 | ☐ |

- [ ] **环境变量配置完整**：

| 变量名 | 类型 | 必需 | 说明 | 状态 |
|-------|------|------|------|------|
| `GITHUB_TOKEN` | Secret | ✅ | GitHub API 访问令牌 | ☐ |
| `LLM_API_KEY` | Secret | ✅ | 大模型 API 密钥 | ☐ |
| `LLM_API_URL` | Config | ✅ | API 端点 URL | ☐ |
| `LLM_MODEL_ID` | Config | ✅ | 模型标识符 | ☐ |
| `MEMORY_ROOT` | Config | ❌ | 业务数据根目录（默认：`.storage/`） | ☐ |
| `WORKFLOW_TIMEOUT` | Config | ❌ | 超时时间（默认：600秒） | ☐ |
| `LOG_LEVEL` | Config | ❌ | 日志级别（默认：`INFO`） | ☐ |
| `NOTIFICATION_WEBHOOK` | Secret | ❌ | 失败通知 Webhook URL | ☐ |

- [ ] **超时控制配置正确**：

| 阶段 | 超时时间 | 状态 |
|-----|---------|------|
| 整体工作流 | 10 分钟（可配置） | ☐ |
| 数据收集阶段 | 120 秒 | ☐ |
| 大模型处理阶段 + GraphQL 映射 | 300 秒 | ☐ |
| 存储写入阶段 | 30 秒 | ☐ |
| Issue 回写阶段 | 60 秒 | ☐ |

### §7.3 组件 2: Issue Tracker 回写机制验证
- [ ] **回写流程三阶段完整**：
  - [ ] Phase 1: 数据提取（reviewId, coreConclusion ≤150 字符, issueUrl）
  - [ ] Phase 2: Issue 定位（通过 Issue Tracker API）
  - [ ] Phase 3: 评论写入（GraphQL Mutation Payload 格式）
- [ ] **评论格式标准**：
  - [ ] 标题：`📋 **复盘记录自动生成**`
  - [ ] reviewId 显示正确（`` `REV-XXXXXX-XXX` `` 格式）
  - [ ] coreConclusion 显示正确（≤150 字符）
  - [ ] 详情查看链接指向正确的 `.md` 文件相对路径
  - [ ] 底部包含 ISO 8601 时间戳
- [ ] **Fallback Chain 实现**：
  - [ ] Level 1: issueUrl 字段有效时直接使用
  - [ ] Level 2: 从 PR/MR 描述解析 `Fixes #xxx` / `Closes #xxx` / `Resolves #xxx`
  - [ ] Level 3: 从 PR/MR 的 `linked_issues` API 字段获取
  - [ ] Level 4: 所有方法失败时跳过回写并记录 WARN 日志（不阻塞主流程）
- [ ] **容错与重试机制**：

| HTTP 状态码 | 错误类型 | 处理策略 | 状态 |
|------------|---------|---------|------|
| 401 | 认证失败 | ❌ 立即终止 + 发送通知 | ☐ |
| 403 | 权限不足 | ❌ 立即终止 + 建议检查权限 | ☐ |
| 404 | 资源不存在 | ⚠️ Warn 日志 + 跳过（不阻塞） | ☐ |
| 429 | 速率限制 | 🔄 指数退避重试（最多 5 次） | ☐ |
| 5xx | 服务器错误 | 🔄 固定间隔重试（最多 3 次） | ☐ |
| N/A | 网络超时 | 🔄 重试（最多 3 次，每次 30s） | ☐ |

### §7.4 双向追溯性保障验证
- [ ] **向上追溯**：复盘记录 → PR/MR 页面（prUrl 可点击跳转，查看完整讨论和 Diff）
- [ ] **向下穿透**：Issue → 复盘评论（自动添加评论含 reviewId 和核心结论）
- [ ] **横向关联**：关键词 → 相关记录（`@skill 查询记忆` 可检索到关联记录）

---

## Phase 8: 上下文注入系统验证（Automated Context Injection System Verification）

### §8.1 架构总览验证
- [ ] **IDE 集成层**：
  - [ ] 文件事件监听器（FE）
  - [ ] 请求拦截器（RI）
  - [ ] 提示注入器（TI）
- [ ] **核心引擎（GraphQL-Powered）**：
  - [ ] 故障历史检测器（FH）
  - [ ] 智能查询引擎（IQ — GraphQL Query Builder）
  - [ ] 相关性分析器（CA ≥85%）
  - [ ] 上下文注入器（CI）

### §8.2 组件 1: 防错预警模块验证
- [ ] **检测算法流程四步骤完整**：
  - [ ] Step 1: 路径匹配 → 提取文件名和模块路径作为 keywords
  - [ ] Step 2: 故障标签过滤 → 过滤包含 bug/incident/crash 等标签的记录
  - [ ] Step 3: 关联路径匹配 → 精确路径匹配 + 模糊匹配（模块名/类名/函数名）
  - [ ] Step 4: 风险评分计算 → 多因子加权评分模型
- [ ] **风险评分模型四因子权重正确**：

| 因子 | 权重 | 说明 | 状态 |
|-----|------|------|------|
| 故障记录数量 | 40% | 该文件相关的 bug/incident 记录数 | ☐ |
| 故障严重程度 | 25% | crash/deadlock > timeout/warning | ☐ |
| 时间新鲜度 | 20% | 近期故障（30天）权重高于历史故障 | ☐ |
| 复现频率 | 15% | 同类问题重复出现次数 | ☐ |

- [ ] **高风险判定标准**：
  - [ ] 🟢 低风险：`risk_score < 30` → 无提示
  - [ ] 🟡 中风险：`30 ≤ score < 60` → Info 级别提示
  - [ ] 🔴 高风险：`score ≥ 60` → Warning 级别 + 详细建议
- [ ] **提示格式标准**：
  - [ ] 包含标题：⚠️ [系统性复盘预警] 文件风险评估报告
  - [ ] 包含元数据：📁 目标文件, 🔢 风险评分(xxx/100), 🐛 历史故障数, 🏷️ 主要故障类型
  - [ ] 包含推荐最佳实践（每条含内容 + 来源 reviewId）
  - [ ] 包含详情查看指引：@skill 查询记忆 {keywords}
- [ ] **性能要求达标**：

| 指标 | 目标值 | 状态 |
|-----|-------|------|
| 插件加载时间 | ≤500ms | ☐ |
| 文件检测响应时间 | ≤300ms | ☐ |
| 内存占用 | ≤50MB | ☐ |
| CPU 占用 | ≤5% | ☐ |

### §8.3 组件 2: 无感挂载模块验证
- [ ] **智能查询流程四步骤完整**：
  - [ ] Step 1: Prompt 意图分析（关键词提取 + 任务类型识别 + 复杂度估算）
  - [ ] Step 2: 隐式 GraphQL Query 构建（Variables + Field Selection + 三阶段检索）
  - [ ] Step 3: 相关性分析与筛选（四维评分 + 硬阈值过滤 ≥0.85 + Top 3 选择）
  - [ ] Step 4: 上下文构建与注入（Best Practices 提炼 + System Prompt 增强 + 透明注入）
- [ ] **透明化设计原则全面落实**：

| 原则 | 说明 | 状态 |
|-----|------|------|
| **无感注入** | 整个过程对用户完全透明，无需额外操作 | ☐ |
| **零延迟感知** | 后台并行执行（≤300ms），不增加等待时间 | ☐ |
| **可覆盖** | 用户声明"忽略历史经验"时可禁用 | ☐ |
| **可追溯** | 每条注入内容包含来源 `reviewId` | ☐ |
| **非侵入式** | 附加在 System Prompt 末尾，不修改原始 Prompt | ☐ |

### §8.4 IDE 兼容性矩阵验证
- [ ] **各 IDE 平台支持情况**：

| IDE / 平台 | 防错预警 | 无感挂载 | 集成方式 | 状态 |
|-----------|---------|---------|---------|------|
| VS Code | ✅ 完整支持 | ✅ 完整支持 | Extension API | ☐ |
| Trae IDE | ✅ 完整支持 | ✅ 完整支持 | Plugin SDK | ☐ |
| JetBrains IDEA | 🟡 部分 | 🟡 部分 | IntelliJ Platform Plugin | ☐ |
| Vim/Neovim | ⚠️ 实验 | ⚠️ 实验 | LSP Client + autocmd | ☐ |
| Cursor/Windsurf | ✅ 完整 | ✅ 完整 | 兼容 VS Code API | ☐ |

### §8.5 数据安全与隐私保护验证
- [ ] **本地存储优先**：所有数据存储在本地 `.storage/` 和 `.cache/`
- [ ] **敏感信息管理**：API Key 通过 Keychain 或环境变量管理，禁止明文
- [ ] **审计日志**：记录所有数据访问操作（时间戳、操作者、操作类型、对象）
- [ ] **数据脱敏**：日志中敏感字段仅显示前 4 位 + `...`
- [ ] **用户同意**：首次使用时弹出数据使用说明并获得确认
- [ ] **一键清除**：提供清除所有本地缓存和历史数据的选项

### §8.6 效果评估指标验证
- [ ] **效率指标达标**：

| 指标 | 目标值 | 测量方法 | 状态 |
|-----|-------|---------|------|
| 上下文命中率 | ≥70% | AI 输出中引用注入内容的比例 | ☐ |
| 问题预防率 | ≥60% | 开启/关闭预警后的 Bug 数量对比 | ☐ |
| 查询加速比 | ≥1.5x | 有/无注入的任务耗时对比 | ☐ |
| 用户干预减少率 | ≥50% | 手动查询频率下降比例 | ☐ |

- [ ] **质量指标达标**：

| 指标 | 目标值 | 测量方法 | 状态 |
|-----|-------|---------|------|
| 代码规范合规率 | ≥80% | Code Review 评价统计 | ☐ |
| 反模式检出率 | ≥85% | 测试集通过率 | ☐ |
| 相关性准确率 | ≥85% | 人工标注一致性对比 | ☐ |
| 误报率 | ≤10% | 随机样本审核统计 | ☐ |

---

## Phase 9: 记忆生命周期与知识图谱验证（Memory Lifecycle & Knowledge Graph Verification）

### §9.1 架构总览验证
- [ ] **记忆生命周期管理**：
  - [ ] 定期巡检脚本（IN）
  - [ ] 衰减检测器（DA）
  - [ ] 分类筛选器（CA）
  - [ ] 评估引擎（EA）
  - [ ] 归档建议生成器（AR）
- [ ] **知识图谱构建（GraphQL-native）**：
  - [ ] 实体识别引擎（ER）
  - [ ] 关系抽取机制（RE）
  - [ ] GraphQL Schema 存储（GS）
  - [ ] 可视化平台（VIZ）
- [ ] **Review Node 与知识图谱的关系明确**：

| 关系类型 | 连接方式 | 说明 | 状态 |
|---------|---------|------|------|
| **图谱节点** | `Review` 实现 `Node` 接口 | 每个 Review 是知识图谱的一个锚点 | ☐ |
| **向上追溯** | `issueUrl` / `prUrl` Edge | Review → GitHub Issue/PR 页面 | ☐ |
| **向下穿透** | Issue Comment 回写 | Issue → 复盘评论（含 reviewId） | ☐ |
| **横向关联** | 关键词检索 + `relatedTo` Edge | Review ↔ Review（语义关联） | ☐ |
| **实体挂载** | `Review` 作为 `ModuleEntity` 的元数据 | 复盘结论挂载到代码模块 | ☐ |

- [ ] **架构定位确认**：Review Node 是知识图谱的**入口点（Entry Point）**而非唯一实体

### §9.2 组件 1: 记忆衰减与归档管理验证
- [ ] **LifecycleMetadata 类型已定义**（GraphQL Type Definition）：
  - [ ] `lastAccessedAt: DateTime` — 最后一次被检索的时间戳
  - [ ] `accessCount: Int!` — 累计被检索次数
  - [ ] `accessFrequency30d: Int!` — 最近 30 天内的检索次数
  - [ ] `accessFrequency90d: Int!` — 最近 90 天内的检索次数
  - [ ] `accessTrend: AccessTrend!` — 访问趋势（RISING / STABLE / DECLINING）
  - [ ] `creationAgeDays: Int!` — 创建至今的天数
  - [ ] `category: LifecycleCategory!` — 分类标签
  - [ ] `importanceScore: Float!` — 重要性评分（0.0 - 1.0）
  - [ ] `decayIndicator: Boolean!` — 是否触发衰减指示器
  - [ ] `archiveRecommendation: ArchiveRecommendation` — 归档建议
  - [ ] `archivedAt: DateTime` — 归档时间
  - [ ] `archivedReason: String` — 归档原因
- [ ] **辅助枚举类型已定义**：
  - [ ] `AccessTrend` 枚举：RISING, STABLE, DECLINING
  - [ ] `LifecycleCategory` 枚举：ARCHITECTURE, SECURITY, BUSINESS_LOGIC, UI_FRONTEND, DATA_MODEL, INCIDENT
  - [ ] `ArchiveRecommendation` 枚举：STRONGLY_RECOMMENDED, RECOMMENDED, NOT_RECOMMENDED
- [ ] **衰减检测指标完整**：

| 指标 | GraphQL Field | 计算公式 | 阈值 | 警告级别 | 状态 |
|-----|--------------|---------|------|---------|------|
| 时间老化 | `creationAgeDays` | `> 365` | 超过1年 | ⚠️ 老化警告 | ☐ |
| 访问停滞 | `lastAccessedAt` | 距今 > 180天 | 半年未访问 | 🔴 停滞警告 | ☐ |
| 频率下降 | `freq30d / freq90d` | `< 0.3` | 近期骤降 | 📉 衰减趋势 | ☐ |
| 零引用 | `accessCount` | `= 0` | 从未被检索 | ❌ 孤岛记录 | ☐ |

- [ ] **类别分类与归档策略**：

| LifecycleCategory | 归档策略 | 状态 |
|-------------------|---------|------|
| `ARCHITECTURE`（基础架构） | ⛔ 禁止自动归档（需人工确认） | ☐ |
| `SECURITY`（安全合规） | ⛔ 禁止自动归档（长期保留） | ☐ |
| `BUSINESS_LOGIC`（业务逻辑） | ✅ 可自动归档（低风险） | ☐ |
| `UI_FRONTEND`（UI/前端） | ✅ 可自动归档（低风险） | ☐ |
| `DATA_MODEL`（数据模型） | ⚠️ 需谨慎归档 | ☐ |
| `INCIDENT`（故障处理） | ⚠️ 需保留较长时间（≥2年） | ☐ |

- [ ] **综合评分公式实现正确**（GraphQL Resolver Logic）：
  - [ ] lifecycle_score = importance_weight(0.35) × importanceScore + activity_weight(0.25) × activity_score + connectivity_weight(0.20) × connectivity_score + timeliness_weight(0.20) × timeliness_score
  - [ ] 归档判定逻辑正确：
    - [ ] lifecycle_score < 0.30 → STRONGLY_RECOMMENDED
    - [ ] 0.30 ≤ score < 0.50 → RECOMMENDED
    - [ ] lifecycle_score ≥ 0.50 → NOT_RECOMMENDED

### §9.3 组件 2: 知识图谱构建系统验证（GraphQL-native）
- [ ] **实体类型体系（GraphQL Union / Interface）已定义**：
  - [ ] `GraphEntity` Union Type 包含以下类型：
    - [ ] ModuleEntity, ComponentEntity, APIEntity, DataStructureEntity
    - [ ] FunctionEntity, TechnologyEntity, ConceptEntity
    - [ ] IssueTrackerEntity, PatternEntity, RiskEntity
  - [ ] `ModuleEntity implements GraphNode` 已定义（含 id, name, description, filePath）
  - [ ] 其他实体类型定义类似
- [ ] **关系类型体系（GraphQL Edge / Connection）已定义**：
  - [ ] `GraphConnection` 类型（Connection Pattern — 符合 GraphQL Relay 规范）：
    - [ ] `edges: [GraphEdge!]!`
    - [ ] `pageInfo: PageInfo!`
    - [ ] `totalCount: Int!`
  - [ ] `GraphEdge` 类型（含 cursor, node, relationType, weight, metadata）
  - [ ] `GraphRelationType` 枚举完整：
    - [ ] DEPENDS_ON, CALLS, CONTAINS, USES, RELATED_TO
    - [ ] CAUSES, SOLVED_BY, EVOLVES_TO
- [ ] **图谱存储方案选择评估完成**：

| 方案 | 适用规模 | GraphQL 集成 | 优点 | 缺点 | 状态 |
|-----|---------|------------|------|------|------|
| **A: SDL 文件 + Resolver** | < 10K 实体 | 原生支持 | 无额外依赖，Git 友好 | 大规模查询性能有限 | ☐ |
| **B: PostgreSQL + pg_graphql** | 10K-100K | 通过 `@pg` directive | 成熟稳定，事务支持好 | 图遍历需递归 CTE | ☐ |
| **C: Neo4j + graphql-neo4j** | > 100K | 原生图算法集成 | 高性能图遍历 | 引入额外依赖 | ☐ |

- [ ] **脆弱点分析模型已实现**（GraphQL Query + Resolver）：
  - [ ] `vulnerabilities` Query 已定义（含 projectId 参数）
  - [ ] vulnerability_score 公式正确：
    - [ ] w1(0.40) × spof_risk + w2(0.35) × failure_cluster_risk + w3(0.25) × chain_risk
  - [ ] RiskLevel 枚举判定逻辑正确：
    - [ ] CRITICAL (≥ 0.80): 立即关注
    - [ ] HIGH (0.60 - 0.80): 纳入技术债务清单
    - [ ] MEDIUM (0.40 - 0.60): 保持监控
    - [ ] LOW (< 0.40): 暂不处理

---

## Phase 10: 测试与验证方案验证（Testing & Verification Verification）

### §10.1 MyST 格式基础测试验证（5 个 Test Cases）
- [ ] **TC1: 模板生成正确性**：
  - [ ] 验证目标：MyST 文件创建与 GraphQL Schema 映射
  - [ ] 关键检查点：YAML Front Matter 完整、5 个 Admonition 存在、核心结论 ≤150 字符
- [ ] **TC2: MD → GraphQL 转换**：
  - [ ] 验证目标：双向转换准确性
  - [ ] 关键检查点：转换后的数据可通过 GraphQL Schema 校验、字段映射正确、无数据丢失
- [ ] **TC3: GraphQL → MD 反向转换**：
  - [ ] 验证目标：转换一致性
  - [ ] 关键检查点：MD 通过合规校验、语义等价、字段值一致
- [ ] **TC4: GraphQL Schema 合规性校验**：
  - [ ] 验证目标：验证脚本准确率
  - [ ] 关键检查点：PASS/WARN/FAIL 判定正确、误判率 ≤5%
- [ ] **TC5: 单格式存储一致性**：
  - [ ] 验证目标：端到端验证
  - [ ] 关键检查点：写入 MD → Schema 校验 → 读取 → 再校验流程完整、异常降级正常

### §10.2 核心功能测试验证（5 个 Test Cases）
- [ ] **TC1: 完整复盘流程**：
  - [ ] 验证目标：createReview Mutation
  - [ ] Input: 复杂上下文
  - [ ] Validate: GraphQL Schema 合规 + reviewId 格式正确 + 返回 ≤10 行
- [ ] **TC2: 参数化查询**：
  - [ ] 验证目标：reviews Query
  - [ ] Input: 关键词+时间+类型组合
  - [ ] Validate: Top 3 返回 + 每条 ≤2 行 + 相关度排序合理
- [ ] **TC3: 字段级更新与归档**：
  - [ ] 验证目标：updateReview / archiveReview Mutations
  - [ ] Input: 数组追加+字符串覆写+状态变更
  - [ ] Validate: Diff 输出正确 + Schema 完整性保持
- [ ] **TC4: 图关系追溯**：
  - [ ] 验证目标：Graph Traversal
  - [ ] Input: 含 URL 的记录创建+反向查询
  - [ ] Validate: URL 格式验证 + 关联 Query 正确
- [ ] **TC5: 向后兼容性**：
  - [ ] 验证目标：Schema Evolution
  - [ ] Input: 旧版本记录 + 新版 Schema 读取
  - [ ] Validate: 兼容层映射 + 无报错 + 数据完整

### §10.3 量化断言（Assertions）验证
- [ ] **GraphQL Schema 合规性断言（5 项）全部实现**：
  - [ ] ✅ required_fields_present: 所有标记为 `!` 的字段非空（NonNull Constraint）
  - [ ] ✅ review_id_format_match: 匹配自定义标量 ReviewID 的正则约束
  - [ ] ✅ timestamp_iso8601: 符合自定义标量 DateTime 的 ISO 8601 格式
  - [ ] ✅ enum_values_valid: status/taskType 在预定义 Enum 范围内
  - [ ] ✅ no_extra_fields: Schema 中未定义的字段被拒绝（Strict Validation）
- [ ] **输出契约断言（Field Selection 断言）（4 项）全部实现**：
  - [ ] ✅ review_output_lines ≤ 10
  - [ ] ✅ query_result_per_item ≤ 2
  - [ ] ✅ no_full_object_expansion_in_output（禁止 `{ review { ... on Review { * } } }`）
  - [ ] ✅ diff_only_for_updates（Mutation 仅返回 changeSummary）
- [ ] **工具白名单断言（3 项）全部实现**：
  - [ ] ✅ only_whitelisted_tools_used
  - [ ] ✅ no_shell_commands
  - [ ] ✅ read_with_offset_limit（Cursor-based Pagination）
- [ ] **GraphQL 错误处理断言（3 项）全部实现**：
  - [ ] ✅ error_extensions_format_valid（符合 GraphQL Error Extensions 规范）
  - [ ] ✅ hint_actionable（extensions.hint 字段可操作）
  - [ ] ✅ all_5_error_codes_covered

### §10.4 集成测试验证清单
- [ ] 技能在 Trae IDE 环境中正常加载（SKILL.md 解析无误）
- [ ] 三条 Mutations（createReview/updateReview/archiveReview）和一条 Query（reviews）均可正确触发并产生合法输出
- [ ] 工具白名单约束有效执行（违规检测率 = 0%）
- [ ] 跨平台路径处理正确（Windows/macOS 至少 2 个平台）
- [ ] Git 协作场景验证通过（`.storage/` 可 track，`.cache/` 被 ignore）
- [ ] 与其他技能兼容（doc-coauthoring、pdf、xlsx 等）
- [ ] GraphQL Schema 可通过 `graphql validate` 或 `graphqxl` 工具校验
- [ ] GraphQL Introspection Query 返回正确的类型信息

### §10.5 质量门禁（Quality Gates）验证
- [ ] **Phase 1: 基础架构**：
  - [ ] SKILL.md < 500 行
  - [ ] `schema.graphql` 可通过 GraphQL Validator 校验
  - [ ] 目录权限正常
- [ ] **Phase 2: 核心功能**：
  - [ ] 三条 Mutations + 一条 Query 独立执行且输出合规
  - [ ] Schema 校验零错误率 100%
- [ ] **Phase 3: 约束控制**：
  - [ ] 白名单违规检测率 0%
  - [ ] 五大错误码全覆盖
  - [ ] Token 消耗合理
- [ ] **Phase 4: 测试验证**：
  - [ ] 测试通过率 ≥ 90%
  - [ ] 集成测试零阻塞性问题
  - [ ] 跨平台兼容验证通过

---

## Phase 11: 附录验证（Appendix Verification）

### §11.1 GraphQL 设计理念完整落地对照表验证
- [ ] **20 项 GraphQL 理念全部在本技能中落地**：

| # | GraphQL 理念 | 本技能中的体现 | 验证要点 | 状态 |
|---|-------------|--------------|---------|------|
| 1 | **Type System (SDL)** | `schema.graphql` 完整定义所有类型、枚举、接口、联合 | Schema 可被 `graphql validate` 自动校验 | ☐ |
| 2 | **Custom Scalars** | `ReviewID`、`DateTime` 自定义标量带正则约束 | 标量值通过 `@specifiedBy` 和 resolver 验证 | ☐ |
| 3 | **Enums** | `ReviewStatus`、`TaskType`、`GraphRelationType` 等强类型枚举 | 枚举值通过 Introspection 查询 | ☐ |
| 4 | **Interfaces** | `Node` 全局接口、`GraphNode` 图节点接口 | `implements` 约束通过 Schema 校验 | ☐ |
| 5 | **Unions** | `GraphEntity` 联合类型支持多态查询 | `... on TypeName` Fragment 匹配 | ☐ |
| 6 | **Input Types** | `CreateReviewInput`、`UpdateReviewInput` 强类型输入 | Mutation 参数通过 Input Type 校验 | ☐ |
| 7 | **Query/Mutation Separation** | `type Query` vs `type Mutation` 清晰分离 | 读操作无副作用，写操作有副作用 | ☐ |
| 8 | **Field Selection** | Token 优化的极致体现 | 仅返回 Query 中选择的字段 | ☐ |
| 9 | **Arguments with Defaults** | `reviews(limit: Int = 3, status: ReviewStatus = ACTIVE)` | 默认值简化常见查询 | ☐ |
| 10 | **Fragments** | 标准化输出模板（`coreConclusion` + `actionItems[0]`） | Fragment 复用减少重复 | ☐ |
| 11 | **Nullability (!)** | `String!`、`[String!]!` 非 Null 约束 | 编译时 + 运行时双重检查 | ☐ |
| 12 | **Payload Pattern** | `CreateReviewPayload`、`UpdateReviewPayload` 等 | Mutation 返回结构化载荷 | ☐ |
| 13 | **Schema as Contract** | 错误码体系 + 输出契约 + Introspection | 团队共识文档化 + 自动文档 | ☐ |
| 14 | **Graph Thinking** | `issueUrl`/`prUrl` Edge + 知识图谱 Union/Connection | 原生图遍历能力 | ☐ |
| 15 | **Business Logic Layer** | 复盘分析引擎作为中心 Resolver | 唯一正确来源（Single Source of Truth） | ☐ |
| 16 | **Introspection** | `__schema`、`__type` 查询支持 | 自动生成文档，保证一致性 | ☐ |
| 17 | **Backward Compatibility** | Additive Changes + `@deprecated` Directive | 渐进式演进无破坏 | ☐ |
| 18 | **Error Handling** | GraphQL Errors + Extensions（code, hint） | 可预测、可程序化处理 | ☐ |
| 19 | **Pagination (Connection)** | `limit: Int = 3` + offset/limit 读取 | 3 节点 × 120 行硬阈值 | ☐ |
| 20 | **Deprecation** | `@deprecated(reason: "...")` 三阶段渐进 | 平滑过渡无突变 | ☐ |
| 21 | **Directives** | `@deprecated`、`@specifiedBy`、`@versioned` | 元编程能力 | ☐ |
| 22 | **Variables** | `$input: CreateReviewInput!` 强类型变量 | 注入攻击防护 | ☐ |

### §11.2 目录结构与文件说明验证（GraphQL-Native）
- [ ] **目录结构完整且符合 spec 定义**：
  ```
  project-root/
  ├── .storage/
  │   └── reviews/                    # 业务数据（纳入 Git 版本控制）
  │       ├── REV-20260417-001.md     # MyST Markdown 主文件（唯一存储格式）
  │       └── _archive/               # 归档目录
  ├── .cache/
  │   └── reviews/                    # 缓存数据（加入 .gitignore）
  ├── src/
  │   └── schema.graphql              # ★ GraphQL SDL 数据契约定义
  ├── templates/
  │   └── review_template.myst        # MyST 复盘记录标准模板
  ├── tools/
  │   ├── md_graphql_converter.py     # ★ MyST MD ↔ GraphQL 双向转换工具
  │   └── validate_graphql_schema.py  # ★ GraphQL Schema 合规性校验脚本
  ├── scripts/                        # CI/CD 自动化脚本
  │   ├── auto_review_pipeline.py     # 主流程编排
  │   ├── data_collector.py           # 数据收集模块
  │   ├── llm_processor.py            # 大模型处理模块 + GraphQL 映射
  │   ├── storage_manager.py          # 存储管理模块（MyST MD 读写）
  │   ├── issue_extractor.py          # Issue 数据提取
  │   ├── issue_writer.py             # Issue 评论写入
  │   ├── retry_handler.py            # 容错与重试
  │   ├── logger.py                   # 日志记录
  │   └── notifier.py                 # 失败通知
  ├── plugins/                        # IDE 插件（上下文注入系统）
  │   ├── failure_detector.py         # 故障历史检测
  │   ├── tooltip_injector.py         # 智能提示注入
  │   ├── request_interceptor.py      # 请求拦截器（GraphQL Query 拦截）
  │   ├── intent_analyzer.py          # Prompt 意图分析
  │   ├── smart_query_engine.py       # ★ GraphQL Query Builder
  │   ├── correlation_analyzer.py     # 相关性分析
  │   ├── context_injector.py         # 上下文注入
  │   ├── plugin_manager.py           # 插件管理器
  │   └── metrics_collector.py        # 效果评估指标采集
  └── SKILL.md                        # 技能主文件（Prompt 定义）
  ```
- [ ] **关键变更确认**：
  - [ ] `memory-schema.json` → **`schema.graphql`**（GraphQL SDL 替代 JSON Schema）
  - [ ] `md_json_converter.py` → **`md_graphql_converter.py`**（GraphQL 转换工具）
  - [ ] `validate_myst.py` → **`validate_graphql_schema.py`**（GraphQL Schema 校验）
  - [ ] 移除辅助 `.json` 文件，采用单格式存储（MyST MD + GraphQL Schema 映射）

### §11.3 术语表验证（Glossary - GraphQL-Centric）
- [ ] **22 项核心术语定义完整**：

| 术语 | 全称 | 定义是否完整 | 状态 |
|-----|------|-------------|------|
| **GraphQL** | Graph Query Language | ☐ | |
| **SDL** | Schema Definition Language | ☐ | |
| **Scalar** | Scalar Type | ☐ | |
| **Enum** | Enumeration Type | ☐ | |
| **Interface** | Interface Type | ☐ | |
| **Union** | Union Type | ☐ | |
| **Input Type** | Input Type | ☐ | |
| **Mutation** | Mutation Operation | ☐ | |
| **Query** | Query Operation | ☐ | |
| **Resolver** | Resolver Function | ☐ | |
| **Payload Pattern** | Mutation Payload Pattern | ☐ | |
| **Introspection** | Introspection | ☐ | |
| **Field Selection** | Field Selection | ☐ | |
| **Fragment** | Fragment | ☐ | |
| **Variable** | Variable | ☐ | |
| **Directive** | Directive | ☐ | |
| **Nullability** | Non-Null Marker (!) | ☐ | |
| **Connection** | Connection Pattern | ☐ | |
| **MyST** | Markedly Structured Text | ☐ | |
| **Admonition** | Admonition Block | ☐ | |
| **Front Matter** | YAML Front Matter | ☐ | |
| **AST** | Abstract Syntax Tree | ☐ | |

---

## 质量门禁通过标准汇总（Quality Gates Summary）

### 各 Phase 通过标准

| Phase | 名称 | 完成标准 | 状态 |
|-------|------|---------|------|
| **Phase 1** | 概述与设计哲学 | 六大核心理念全部体现 + 变更范围清单完整 + 影响范围确认 | ☐ |
| **Phase 2** | 局限性与解决方案 | 6 大局限性有应对策略 + 8 大 GraphQL 优势已落地 | ☐ |
| **Phase 3** | 核心功能定义 | GraphQL 完整类型系统（Scalar/Enum/Object/Input/Root/Payload）+ 6 大功能模块 + 5 个 Scenario 验证通过 | ☐ |
| **Phase 4** | 数据模型与存储架构 | MyST 模板完整（5 Admonitions + Core Conclusion）+ 9 项合规性校验 + 双格式协同架构确认 | ☐ |
| **Phase 5** | 接口规范与操作流程 | 四种指令识别规则 + 白名单工具集 + 六步 Resolver Pipeline | ☐ |
| **Phase 6** | 约束控制与质量保障 | Token 优化三侧（输入/存储/输出）+ 五大错误码 + 向后兼容四原则 | ☐ |
| **Phase 7** | CI/CD 集成 | GitHub Actions 工作流 + Issue 回写（Fallback Chain 4 级）+ 双向追溯 | ☐ |
| **Phase 8** | 上下文注入系统 | 防错预警（四因子风险评分）+ 无感挂载（五原则透明化）+ IDE 兼容矩阵 + 效果指标（8 项） | ☐ |
| **Phase 9** | 记忆生命周期与知识图谱 | LifecycleMetadata 类型 + 衰减四指标 + 归档六策略 + GraphEntity Union + GraphRelationType 枚举 + 脆弱点分析模型 | ☐ |
| **Phase 10** | 测试与验证方案 | 10 个 Test Cases（5 MyST + 5 核心）+ 15 项量化断言 + 8 项集成测试 + 4 阶段质量门禁 | ☐ |
| **Phase 11** | 附录 | 22 项 GraphQL 理念落地 + 目录结构完整 + 22 项术语表 | ☐ |

---

> **文档版本**: v3.0 (GraphQL-Native Edition)
> **最后更新**: 2026-04-17
> **依据**: spec.md (2098 行, 完整内容 100% 覆盖)
