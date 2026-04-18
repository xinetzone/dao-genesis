# 系统性复盘与记忆管理技能 - 实施任务清单

> **基于**: `spec.md` v3.0 (GraphQL-Native Edition)
> **生成日期**: 2026-04-17
> **总阶段数**: 11 个 Phase | **总任务数**: 68 个主任务 | **子任务数**: 240+
> **技术栈要求**:
> - Python 3.14+ 及更高版本
> - FastAPI 框架（与 Python 3.14+ 兼容）
> - PEP 8 编码规范
> - 完整的功能文档、API 接口说明及单元测试用例

---

## 📋 任务依赖关系图 (Task Dependencies Graph)

```
Phase 1 (Schema) ──────────────────────────────────────────────────────┐
     │                                                                  │
     ├──→ Phase 2 (Converter) ──→ Phase 3 (Validator) ────────────────┤
     │         │                    │                                  │
     │         └──→ Phase 4 (Template) ─┐                             │
     │                                  │                             │
     ├──→ Phase 5 (SKILL.md) ←─────────┘                             │
     │         │                                                       │
     │         ├──→ Phase 6 (Core Engine) ◄───────────────────────────┤
     │         │         │                                            │
     │         │         ├──→ Phase 7 (Token Optimizer)               │
     │         │         │         │                                 │
     │         │         ├──→ Phase 8 (CI/CD)                        │
     │         │         │         │                                 │
     │         │         ├──→ Phase 9 (Context Injection)             │
     │         │         │         │                                 │
     │         │         └──→ Phase 10 (Lifecycle & KG)              │
     │         │                   │                                │
     │         └───────────────────┼────────────────────────────────┤
     │                             │                                │
     └─────────────────────────────┼────────────────────────────────┤
                                   ▼                                │
                          Phase 11 (Testing & Verification) ◄────────┘
```

## ⚡ 并行执行策略 (Parallel Execution Strategy)

| 批次 | 可并行执行的 Phase | 前置条件 | 预计耗时 |
|-----|-------------------|---------|---------|
| **Batch 1** | Phase 1, Phase 4 | 无 | 基础架构搭建 |
| **Batch 2** | Phase 2, Phase 3, Phase 5 | Phase 1 完成 | 核心组件开发 |
| **Batch 3** | Phase 6, Phase 7 | Phase 2 + Phase 5 完成 | 功能实现 |
| **Batch 4** | Phase 8, Phase 9, Phase 10 | Phase 6 完成 | 扩展功能 |
| **Batch 5** | Phase 11 | 所有前置 Phase 完成 | 测试验证 |

---

## ✅ 质量门禁 (Quality Gates)

| Gate ID | 触发时机 | 通过标准 | 阻断级别 |
|---------|---------|---------|---------|
| **QG-01** | Phase 1 完成后 | `schema.graphql` 可通过 `graphql validate` 校验；包含所有 Scalar/Enum/Object/Input/Root/Payload Types | 🔴 阻塞性 |
| **QG-02** | Phase 2-3 完成后 | 转换器双向转换准确率 ≥ 98%；校验脚本误判率 ≤ 5% | 🔴 阻塞性 |
| **QG-03** | Phase 4-5 完成后 | 模板与 Schema 映射 100% 一致；SKILL.md < 500 行；指令解析准确率 ≥ 95% | 🔴 阻塞性 |
| **QG-04** | Phase 6-7 完成后 | 四条操作（3 Mutation + 1 Query）独立执行且输出合规；Token 消耗在阈值内 | 🔴 阻塞性 |
| **QG-05** | Phase 8-10 完成后 | CI/CD 工作流可触发执行；上下文注入响应时间 ≤ 300ms；归档策略逻辑正确 | 🟡 非阻塞（需记录） |
| **QG-06** | Phase 11 完成后 | 测试通过率 ≥ 90%；集成测试零阻塞性问题；跨平台兼容验证通过 | 🔴 阻塞性 |

---

# Phase 1: GraphQL Schema 定义 (§3.1)

> **目标**: 创建 `src/schema.graphql`，定义完整的 GraphQL 类型系统（SDL）
> **产出物**: `src/schema.graphql`
> **质量门禁**: QG-01

- [ ] **Task 1.1: 创建项目目录结构**
  - [ ] 1.1.1 创建 `src/` 目录
  - [ ] 1.1.2 创建 `.storage/reviews/` 目录（业务数据存储）
  - [ ] 1.1.3 创建 `.storage/reviews/_archive/` 目录（归档数据）
  - [ ] 1.1.4 创建 `.cache/reviews/` 目录（缓存数据）
  - [ ] 1.1.5 创建 `templates/` 目录
  - [ ] 1.1.6 创建 `tools/` 目录
  - [ ] 1.1.7 创建 `scripts/` 目录
  - [ ] 1.1.8 创建 `plugins/` 目录
  - [ ] 1.1.9 配置 `.gitignore`（`.cache/` 纳入忽略列表）

- [ ] **Task 1.1.10: 项目依赖配置（TOML 规范）**
  - [ ] 1.1.10.1 创建 `pyproject.toml` 文件，遵循 PEP 621 规范
  - [ ] 1.1.10.2 配置 Python 版本要求：`requires-python = ">=3.14"`
  - [ ] 1.1.10.3 在 `[project]` 区块配置项目元数据（name, version, description）
  - [ ] 1.1.10.4 在 `[dependencies]` 区块添加 FastAPI 框架依赖
  - [ ] 1.1.10.5 在 `[project.optional-dependencies]` 区块配置开发依赖（dev 分组）
  - [ ] 1.1.10.6 在 `[tool.black]` 区块配置代码格式化规则
  - [ ] 1.1.10.7 在 `[tool.mypy]` 区块配置类型检查规则
  - [ ] 1.1.10.8 在 `[tool.pytest.ini_options]` 区块配置测试选项
  - [ ] 1.1.10.9 配置敏感信息使用 `${VAR}` 环境变量引用（禁止硬编码）

- [ ] **Task 1.2: 定义自定义标量类型 (Custom Scalar Types)**
  - [ ] 1.2.1 定义 `ReviewID` 标量类型
    - 格式约束：`REV-YYYYMMDD-NNN`
    - 正则表达式：`^REV-[0-9]{8}-[0-9]{3}$`
    - 添加 `@specifiedBy(url: ...)` directive
    - 添加详细注释说明（含示例）
  - [ ] 1.2.2 定义 `DateTime` 标量类型
    - ISO 8601 格式：`2026-04-17T08:24:00Z`
    - 添加 `@specifiedBy(url: "http://tools.ietf.org/html/rfc3339")` directive
    - 添加详细注释说明（含示例）

- [ ] **Task 1.3: 定义枚举类型 (Enumeration Types)**
  - [ ] 1.3.1 定义 `ReviewStatus` 枚举
    - `ACTIVE`: 活跃状态（默认值），记录可被检索和更新
    - `ARCHIVED`: 已归档状态，记录仅可读不可修改
    - 为每个值添加中文注释说明
  - [ ] 1.3.2 定义 `TaskType` 枚举
    - `FEATURE_IMPLEMENTATION`: 功能实现
    - `BUG_FIX`: Bug 修复
    - `REFACTORING`: 代码重构
    - `ARCHITECTURE_UPGRADE`: 架构升级
    - `INCIDENT_RESOLUTION`: 故障处理
    - `TECH_DECISION`: 技术决策
    - `OTHER`: 其他类型
    - 为每个值添加中文注释说明

- [ ] **Task 1.4: 定义接口类型 (Interface Type): Node**
  - [ ] 1.4.1 定义全局节点接口 `Node`
    - 字段：`id: ID!`（全局唯一标识符）
    - 符合 GraphQL Relay 规范
    - 为未来 GraphQL Relay 规范兼容预留
    - 添加详细注释说明

- [ ] **Task 1.5: 定义核心对象类型 (Object Type): Review**
  - [ ] 1.5.1 实现 `Node` 接口（`implements Node`）
  - [ ] 1.5.2 定义必填字段（NonNull Fields）
    - `id: ID!` - 全局唯一标识符
    - `reviewId: ReviewID!` - 业务标识符
    - `timestamp: DateTime!` - 创建时间戳
    - `participants: [String!]!` - 参与者列表
    - `taskType: TaskType!` - 任务类型
    - `decisions: [String!]!` - 关键决策列表
    - `successFactors: [String!]!` - 成功因素列表
    - `failureReasons: [String!]!` - 失败原因列表
    - `bestPractices: [String!]!` - 最佳实践列表
    - `actionItems: [String!]!` - 行动项列表
    - `status: ReviewStatus!` - 当前状态（默认：ACTIVE）
  - [ ] 1.5.3 定义可选字段（Optional Fields）
    - `schemaVersion: String` - Schema 版本号（默认："1.2"）
    - `issueUrl: String` - 关联 Issue URL
    - `prUrl: String` - 关联 PR/MR URL
    - `projectId: String` - 项目标识
    - `tags: [String!]` - 标签列表
    - `coreConclusion: String` - 核心结论摘要（≤150 字符）
  - [ ] 1.5.4 为每个字段添加详细注释（中文 + 示例）

- [ ] **Task 1.6: 定义输入类型 (Input Types)**
  - [ ] 1.6.1 定义 `CreateReviewInput` 输入类型
    - 必填字段：`participants`, `taskType`, `decisions`, `successFactors`, `failureReasons`, `bestPractices`, `actionItems`
    - 可选字段：`issueUrl`, `prUrl`, `projectId`, `tags`
    - 为每个字段添加注释说明
  - [ ] 1.6.2 定义 `UpdateReviewInput` 输入类型（Partial Update Pattern）
    - 必填字段：`reviewId: ReviewID!`
    - 数组追加字段：`decisionsAppend`, `successFactorsAppend`, `failureReasonsAppend`, `bestPracticesAppend`, `actionItemsAppend`
    - 字符串覆写字段：`taskTypeOverride`, `statusOverride`, `issueUrlOverride`, `prUrlOverride`
    - 注释说明部分更新模式的设计意图

- [ ] **Task 1.7: 定义查询根类型 (Query Root Type)**
  - [ ] 1.7.1 定义 `reviews` 查询字段
    - 参数：`keywords: [String]`, `taskType: TaskType`, `status: ReviewStatus = ACTIVE`, `dateFrom: DateTime`, `dateTo: DateTime`, `projectId: String`, `limit: Int = 3`
    - 返回类型：`[Review!]!`
    - 支持多维度过滤和分页
  - [ ] 1.7.2 定义 `review` 查询字段
    - 参数：`id: ReviewID!`
    - 返回类型：`Review`（可为 null）
  - [ ] 1.7.3 定义 `node` 查询字段（Relay 兼容）
    - 参数：`id: ID!`
    - 返回类型：`Node`

- [ ] **Task 1.8: 定义变更根类型 (Mutation Root Type)**
  - [ ] 1.8.1 定义 `createReview` Mutation
    - 参数：`input: CreateReviewInput!`
    - 返回类型：`CreateReviewPayload!`
  - [ ] 1.8.2 定义 `updateReview` Mutation
    - 参数：`input: UpdateReviewInput!`
    - 返回类型：`UpdateReviewPayload!`
  - [ ] 1.8.3 定义 `archiveReview` Mutation
    - 参数：`reviewId: ReviewID!`
    - 返回类型：`ArchiveReviewPayload!`

- [ ] **Task 1.9: 定义 Payload 类型 (Mutation Payload Pattern)**
  - [ ] 1.9.1 定义 `CreateReviewPayload` 类型
    - 字段：`review: Review`, `clientMutationId: String`
  - [ ] 1.9.2 定义 `UpdateReviewPayload` 类型
    - 字段：`review: Review`, `changeSummary: String`, `clientMutationId: String`
  - [ ] 1.9.3 定义 `ArchiveReviewPayload` 类型
    - 字段：`review: Review`, `previousStatus: ReviewStatus`, `clientMutationId: String`

- [ ] **Task 1.10: Schema 文件完整性校验**
  - [ ] 1.10.1 验证所有类型定义语法正确性
  - [ ] 1.10.2 验证字段引用关系一致性
  - [ ] 1.10.3 验证 Non-Null 约束标记完整性
  - [ ] 1.10.4 使用 GraphQL Validator 工具进行自动校验（如可用）
  - [ ] 1.10.5 生成 Introspection Query 结果用于文档生成

---

# Phase 2: MyST ↔ GraphQL 双向转换器 (§3.6, tools/md_graphql_converter.py)

> **目标**: 创建 `tools/md_graphql_converter.py`，实现 MyST Markdown 与 GraphQL 类型的双向映射与转换
> **产出物**: `tools/md_graphql_converter.py`
> **质量门禁**: QG-02

- [ ] **Task 2.1: 项目初始化与依赖配置**
  - [ ] 2.1.1 创建 Python 虚拟环境（如需要）
  - [ ] 2.1.2 安装必要依赖包
    - `pyyaml`: YAML Front Matter 解析
    - `graphql-core`: GraphQL Schema 解析与验证
    - `regex`: 高级正则表达式支持
    - `python-frontmatter`: Markdown Front Matter 提取
  - [ ] 2.1.3 创建模块基础结构（类、函数、常量定义区域）

- [ ] **Task 2.2: 字段映射规则实现**
  - [ ] 2.2.1 实现 camelCase ↔ snake_case 转换函数
    - `to_snake_case(camel_case_str)` 函数
    - `to_camel_case(snake_case_str)` 函数
    - 处理特殊情况（缩写词如 ID、URL 等）
  - [ ] 2.2.2 定义字段映射字典（MyST → GraphQL）
    - 基于 §3.6.2 的完整映射表
    - 包含所有 17 个字段的映射规则
  - [ ] 2.2.3 定义反向映射字典（GraphQL → MyST）
    - 与正向映射保持一致性
    - 处理可选字段的默认值

- [ ] **Task 2.3: YAML Front Matter 解析与转换**
  - [ ] 2.3.1 实现 `parse_frontmatter(md_content)` 函数
    - 提取 YAML Front Matter 区域
    - 解析为 Python 字典对象
    - 错误处理（格式错误、编码问题等）
  - [ ] 2.3.2 实现 `frontmatter_to_graphql(frontmatter_dict)` 函数
    - 将 snake_case 字段名转换为 camelCase
    - 类型转换与验证（枚举值、标量格式等）
    - 生成符合 GraphQL Input Type 的字典结构
  - [ ] 2.3.3 实现 `graphql_to_frontmatter(graphql_dict)` 函数
    - 反向转换：camelCase → snake_case
    - 枚举值格式化（大写下划线 → 可读字符串）
    - 生成标准 YAML 格式输出

- [ ] **Task 2.4: MyST Admonition 内容解析**
  - [ ] 2.4.1 实现 Admonition Block 识别与提取
    - 支持 5 种 admonition class：`decision`, `success`, `warning`, `tip`, `important`
    - 正则表达式匹配 `{admonition} :class: xxx` 模式
    - 提取块内文本内容
  - [ ] 2.4.2 实现 Admonition → GraphQL Array 转换
    - 将 admonition 内容解析为字符串数组 `[String!]!`
    - 处理嵌套结构（列表项、加粗文本等）
    - 保留关键信息（权衡考量、否决方案、根因分析等）
  - [ ] 2.4.3 实现 GraphQL Array → Admonition 反向转换
    - 将字符串数组转换为标准 MyST admonition 格式
    - 自动选择正确的 CSS class
    - 保持格式规范性和可读性

- [ ] **Task 2.5: 核心结论处理**
  - [ ] 2.5.1 实现 `extract_core_conclusion(md_content)` 函数
    - 定位文件末尾的 `🎯 核心结论` 部分
    - 提取文本内容（≤150 字符）
    - 验证长度限制
  - [ ] 2.5.2 实现 `validate_core_conclusion(text)` 函数
    - 长度检查（≤150 字符）
    - 内容非空检查
    - 返回验证结果和错误提示

- [ ] **Task 2.6: MD → GraphQL 正向转换流程**
  - [ ] 2.6.1 实现 `md_to_graphql(file_path)` 主函数
    - 步骤 1：读取 MyST Markdown 文件
    - 步骤 2：解析 YAML Front Matter
    - 步骤 3：提取 Admonition 内容
    - 步骤 4：提取核心结论
    - 步骤 5：组装为 GraphQL Review 对象结构
    - 步骤 6：返回转换结果
  - [ ] 2.6.2 实现批量转换支持
    - 支持目录级批量转换
    - 进度显示与错误汇总

- [ ] **Task 2.7: GraphQL → MD 反向转换流程**
  - [ ] 2.7.1 实现 `graphql_to_md(review_obj, template_path)` 主函数
    - 步骤 1：加载 MyST 模板
    - 步骤 2：将 GraphQL 对象转换为 Front Matter 字典
    - 步骤 3：填充 Admonition 区块
    - 步骤 4：写入核心结论
    - 步骤 5：生成完整 MyST Markdown 内容
    - 步骤 6：写入目标文件
  - [ ] 2.7.2 实现模板渲染引擎
    - 支持 Jinja2 风格模板变量替换
    - 条件渲染（可选字段）
    - 循环渲染（数组字段）

- [ ] **Task 2.8: CLI 接口实现**
  - [ ] 2.8.1 实现 `--md-to-graphql` 子命令
    - 参数：输入文件路径、输出格式（JSON/YAML）、详细模式
  - [ ] 2.8.2 实现 `--graphql-to-md` 子命令
    - 参数：输入 JSON/YAML、输出路径、模板路径
  - [ ] 2.8.3 实现 `--validate` 子命令（快速校验模式）
    - 参数：输入文件路径
    - 输出：PASS/WARN/FAIL 结果
  - [ ] 2.8.4 实现 `--batch` 子命令（批量处理模式）
    - 参数：输入目录、输出目录、日志文件

- [ ] **Task 2.9: 错误处理与日志系统**
  - [ ] 2.9.1 定义自定义异常类
    - `ConversionError`: 转换过程错误
    - `MappingError`: 字段映射错误
    - `ValidationError`: 数据验证错误
    - `TemplateError`: 模板渲染错误
  - [ ] 2.9.2 实现分级日志系统
    - DEBUG / INFO / WARN / ERROR 级别
    - 日志格式标准化
    - 支持输出到文件和控制台
  - [ ] 2.9.3 实现错误恢复机制
    - 部分转换失败时的降级处理
    - 错误上下文保留（便于调试）

- [ ] **Task 2.10: 单元测试编写**
  - [ ] 2.10.1 编写字段映射测试用例
    - 测试所有 17 个字段的双向转换正确性
    - 测试边界情况（空值、特殊字符、超长文本）
  - [ ] 2.10.2 编写 Admonition 解析测试用例
    - 测试 5 种 admonition 类型的识别与提取
    - 测试嵌套结构和复杂格式
  - [ ] 2.10.3 编写端到端转换测试用例
    - 使用 spec.md §4.1.2 的完整模板示例作为测试基准
    - 验证 MD → GraphQL → MD 往返转换的一致性
  - [ ] 2.10.4 编写 CLI 命令测试用例
    - 测试各子命令的参数解析和输出格式

---

# Phase 3: GraphQL Schema 合规性校验工具 (tools/validate_graphql_schema.py)

> **目标**: 创建 `tools/validate_graphql_schema.py`，实现对 MyST Markdown 文件的 GraphQL Schema 合规性校验
> **产出物**: `tools/validate_graphql_schema.py`
> **质量门禁**: QG-02

- [ ] **Task 3.1: 校验框架初始化**
  - [ ] 3.1.1 创建 Python 模块基础结构
  - [ ] 3.1.2 加载 `src/schema.graphql` 作为校验规则源
  - [ ] 3.1.3 解析 GraphQL SDL 提取类型定义（使用 graphql-core 库）
  - [ ] 3.1.4 构建校验规则注册表（Validation Registry）

- [ ] **Task 3.2: YAML Front Matter 完整性校验 (`--check-frontmatter`)**
  - [ ] 3.2.1 实现 Required Fields 存在性检查
    - 验证所有标记为 `!` 的 GraphQL 字段在 Front Matter 中存在
    - 必填字段列表：`review_id`, `timestamp`, `participants`, `task_type`, `status`, `decisions`, `success_factors`, `failure_reasons`, `best_practices`, `action_items`
  - [ ] 3.2.2 实现 Non-Null 约束检查
    - 验证必填字段值不为空/null
    - 验证数组字段不为 null（允许空列表 `[]`）
  - [ ] 3.2.3 实现 Field Type 匹配检查
    - 验证字段值类型与 GraphQL 类型定义一致
    - 字符串、整数、布尔、数组类型的区分

- [ ] **Task 3.3: Enum 值有效性校验 (`--check-enums`)**
  - [ ] 3.3.1 实现 `task_type` 枚举值校验
    - 允许值：`Feature Implementation`, `Bug Fix`, `Refactoring`, `Architecture Upgrade`, `Incident Resolution`, `Tech Decision`, `Other`
    - 大小写不敏感匹配
  - [ ] 3.3.2 实现 `status` 枚举值校验
    - 允许值：`active`, `archived`
    - 大小写不敏感匹配
  - [ ] 3.3.3 实现 Enum 值规范化建议
    - 当值不在预定义范围时，提供最接近的建议值

- [ ] **Task 3.4: 自定义标量格式校验 (`--check-scalars`)**
  - [ ] 3.4.1 实现 `review_id` 格式校验
    - 正则表达式：`^REV-[0-9]{8}-[0-9]{3}$`
    - 示例通过：`REV-20260417-001`
    - 示例失败：`REV-2026-001`, `rev-20260417-001`
  - [ ] 3.4.2 实现 `timestamp` 格式校验
    - ISO 8601 格式验证
    - 支持时区信息（Z 或 ±HH:MM）
    - 示例通过：`2026-04-17T10:30:00Z`
  - [ ] 3.4.3 实现 `core_conclusion` 长度校验
    - 最大长度：150 字符
    - 中英文混合字符计数（UTF-8 aware）

- [ ] **Task 3.5: MyST Directive 规范性校验 (`--check-directives`)**
  - [ ] 3.5.1 实现 Admonition Block 存在性检查
    - 验证 5 种必需的 admonition 类型存在：
      - `{admonition} :class: decision` → decisions
      - `{admonition} :class: success` → successFactors
      - `{admonition} :class: warning` → failureReasons
      - `{admonition} :class: tip` → bestPractices
      - `{admonition} :class: important` → actionItems
  - [ ] 3.5.2 实现 Admonition Class 合法性检查
    - 仅允许预定义的 5 种 class 值
    - 检测未知的或拼写错误的 class 名称
  - [ ] 3.5.3 实现 Admonition 内容非空检查
    - 每个 admonition 块必须包含有效内容

- [ ] **Task 3.6: 核心结论存在性校验 (`--check-conclusion`)**
  - [ ] 3.6.1 实现 `🎯 标记检测**
    - 在文件末尾查找核心结论区块
    - 支持变体格式（中英文 emoji 等）
  - [ ] 3.6.2 实现内容长度校验
    - 验证 ≤ 150 字符限制
    - 提供精确的字数统计

- [ ] **Task 3.7: GraphQL 类型映射正确性校验 (`--check-mapping`)**
  - [ ] 3.7.1 实现字段名称映射验证
    - 每个 Front Matter 字段必须对应 GraphQL Schema 中的合法字段
    - 检测多余字段（Schema 中未定义）
    - 检测缺失字段（Schema 要求但 Front Matter 缺少）
  - [ ] 3.7.2 实现字段类型兼容性验证
    - Front Matter 值的类型必须与 GraphQL 类型兼容
    - 数组元素类型检查
  - [ ] 3.7.3 实现 Strict Validation 模式
    - 拒绝 Schema 中未定义的任何额外字段
    - 默认警告模式 vs 严格拒绝模式

- [ ] **Task 3.8: Markdown 语法正确性校验 (`--check-syntax`)**
  - [ ] 3.8.1 实现基本 Markdown 语法检查
    - 损坏链接检测（`[text](url)` 格式）
    - 错误嵌套检测（列表、代码块等）
    - 非法转义字符检测
  - [ ] 3.8.2 实现文件编码检查
    - UTF-8 编码验证
    - LF 行尾符检查（跨平台兼容）
    - BOM（Byte Order Mark）检测

- [ ] **Task 3.9: 综合校验报告生成**
  - [ ] 3.9.1 实现校验结果分级
    - `PASS`: 全部检查通过
    - `WARN`: 有警告但不阻断（建议修复）
    - `FAIL`: 有严重错误（必须修复）
  - [ ] 3.9.2 实现结构化报告输出
    - 控制台彩色输出（✅/⚠️/❌ 图标）
    - JSON 格式输出（用于 CI/CD 集成）
    - 详细错误信息（行号、字段名、预期值、实际值）
  - [ ] 3.9.3 实现校验统计摘要
    - 总检查项数、通过数、警告数、失败数
    - 通过率百分比计算

- [ ] **Task 3.10: CLI 接口与集成**
  - [ ] 3.10.1 实现命令行参数解析
    - `--check-frontmatter`: Front Matter 完整性
    - `--check-enums`: Enum 值有效性
    - `--check-scalars`: 标量格式合规性
    - `--check-directives`: Directive 规范性
    - `--check-conclusion`: 核心结论存在性
    - `--check-mapping`: 类型映射正确性
    - `--check-syntax`: Markdown 语法
    - `--check-all`: 执行全部检查（默认）
    - `--strict`: 严格模式（WARN 也视为 FAIL）
    - `--output-format`: 输出格式（text/json）
  - [ ] 3.10.2 实现单文件校验模式
    - 参数：文件路径
    - 输出：该校验文件的完整报告
  - [ ] 3.10.3 实现批量校验模式
    - 参数：目录路径
    - 输出：汇总报告 + 各文件详情
    - 支持递归子目录
  - [ ] 3.10.4 实现退出码约定
    - 0: 全部 PASS
    - 1: 有 FAIL
    - 2: 仅有 WARN（非 strict 模式下）

---

# Phase 4: MyST 复盘记录标准模板 (templates/review_template.myst)

> **目标**: 创建 `templates/review_template.myst`，定义标准的 MyST Markdown 复盘记录模板
> **产出物**: `templates/review_template.myst`
> **质量门禁**: QG-03

- [ ] **Task 4.1: 模板头部设计 (YAML Front Matter)**
  - [ ] 4.1.1 定义 YAML Front Matter 结构
    - 完全对应 GraphQL Review 类型的所有字段
    - 使用 snake_case 命名（与 GraphQL camelCase 映射）
    - 添加字段注释（说明对应的 GraphQL 字段名和类型）
  - [ ] 4.1.2 定义必填字段占位符
    - `review_id`: `REVIEW_ID_PLACEHOLDER`
    - `timestamp`: `ISO_8601_TIMESTAMP`
    - `participants`: 列表格式示例
    - `task_type`: 枚举值示例
    - `status`: `active`（默认值）
    - 其他必填字段的占位符格式
  - [ ] 4.1.3 定义可选字段占位符
    - `schema_version`: `1.2`（默认值）
    - `pr_url`, `issue_url`: URL 格式示例
    - `project_id`, `tags`: 示例值
    - `core_conclusion`: 空字符串或示例文本

- [ ] **Task 4.2: 元信息区块设计**
  - [ ] 4.2.1 设计元信息展示格式
    - 引用块样式（`>` 开头）
    - 包含创建时间、参与者、状态等关键元信息
    - 从 Front Matter 动态生成
  - [ ] 4.2.2 实现动态变量替换机制
    - 支持 Jinja2 风格模板变量
    - 变量名与 Front Matter 字段一一对应

- [ ] **Task 4.3: 关键决策点 Admonition 设计 (:class: decision)**
  - [ ] 4.3.1 定义 decision admonition 结构
    - 标题：`⚙️ 关键决策点 (Key Decisions)`
    - 支持 `:collapse: true` 折叠属性
    - 决策条目编号列表
  - [ ] 4.3.2 设计决策条目内部结构
    - 决策描述（加粗标题）
    - 权衡考量子列表（✅ 优点 / ❌ 缺点）
    - 被否决的替代方案子列表
  - [ ] 4.3.3 添加 GraphQL 字段映射注释
    - `<!-- 对应 GraphQL 字段：decisions: [String!]! -->`

- [ ] **Task 4.4: 成功因素 Admonition 设计 (:class: success)**
  - [ ] 4.4.1 定义 success admonition 结构
    - 无标题（简洁风格）或自定义标题
    - 成功因素无序列表
  - [ ] 4.4.2 设计成功因素条目格式
    - 简洁描述语句
    - 可包含量化指标（覆盖率、性能数据等）
  - [ ] 4.4.3 添加 GraphQL 字段映射注释

- [ ] **Task 4.5: 失败原因 Admonition 设计 (:class: warning)**
  - [ ] 4.5.1 定义 warning admonition 结构
    - 无标题或自定义标题
    - 失败原因无序列表
  - [ ] 4.5.2 设计失败原因条目格式
    - 问题描述（加粗）
    - 根因分析（缩进子项）
    - 影响范围（可选）
  - [ ] 4.5.3 添加 GraphQL 字段映射注释

- [ ] **Task 4.6: 最佳实践 Admonition 设计 (:class: tip)**
  - [ ] 4.6.1 定义 tip admonition 结构
    - 无标题或自定义标题
    - 最佳实践有序/无序列表
  - [ ] 4.6.2 设计最佳实践条目格式
    - 使用 `{term}` 角色标注关键术语
    - 包含推荐配置/参数
    - 可引用具体 reviewId 作为依据
  - [ ] 4.6.3 添加 GraphQL 字段映射注释

- [ ] **Task 4.7: 行动项 Admonition 设计 (:class: important)**
  - [ ] 4.7.1 定义 important admonition 结构
    - 无标题或自定义标题
    - 行动项任务列表（checkbox 格式 `[ ]`）
  - [ ] 4.7.2 设计行动项条目格式
    - 优先级标记：`[P0 - 紧急]`, `[P1 - 高优]`, `[P2 - 中优]`, `[P3 - 低优]`
    - 任务描述（加粗）
    - 负责人（@mention 格式）
    - 截止日期（ISO 格式或相对时间）
    - 验收标准（缩进子项）
  - [ ] 4.7.3 添加 GraphQL 字段映射注释

- [ ] **Task 4.8: 核心结论区块设计**
  - [ ] 4.8.1 定义核心结论位置
    - 文件末尾，分隔线之后
    - 使用 `***` 分隔符
  - [ ] 4.8.2 设计核心结论格式
    - `🎯 核心结论` 前缀
    - 单段落文本（≤150 字符）
    - 添加字符计数提示
  - [ ] 4.8.3 添加 GraphQL 字段映射注释
    - `<!-- 对应 GraphQL 字段：coreConclusion: String（≤150 字符） -->`

- [ ] **Task 4.9: 模板完整性验证**
  - [ ] 4.9.1 验证所有 GraphQL 字段均有对应模板位置
    - 对照 `schema.graphql` 的 Review 类型逐字段检查
    - 确保无遗漏字段
  - [ ] 4.9.2 验证模板可通过 `validate_graphql_schema.py --check-md` 校验
    - 使用 Phase 3 的校验工具进行自检
    - 修复所有 WARN 和 FAIL 项
  - [ ] 4.9.3 验证模板可被 `md_graphql_converter.py` 正确解析
    - 测试 MD → GraphQL 转换
    - 测试 GraphQL → MD 反向转换（使用模板作为目标格式）

- [ ] **Task 4.10: 模板示例实例化**
  - [ ] 4.10.1 基于模板创建完整示例文件
    - 使用 spec.md §4.1.2 的示例数据
    - 生成 `REV-20260417-001.md` 示例文件
  - [ ] 4.10.2 验证示例文件的所有特性
    - Front Matter 完整性
    - 5 个 Admonition 块正确渲染
    - 核心结论格式正确
    - 整体可读性评估

---

# Phase 5: SKILL.md 主文件实现 (§5.0)

> **目标**: 创建 `SKILL.md`，实现技能的主 Prompt 定义，包含指令解析层、工具白名单、错误处理
> **产出物**: `SKILL.md`
> **质量门禁**: QG-03（SKILL.md < 500 行）

- [ ] **Task 5.1: SKILL.md 文档结构与元信息**
  - [ ] 5.1.1 定义文档头部元信息
    - 技能名称、版本号、最后更新日期
    - 维护者信息
    - 规范版本引用（spec.md v3.0）
  - [ ] 5.1.2 定义章节结构大纲
    - 技能概述
    - 指令参考手册
    - 操作流程指南
    - 工具使用规范
    - 输出契约
    - 错误处理
    - 最佳实践

- [ ] **Task 5.2: 指令解析层实现 (Instruction Parsing Layer)**
  - [ ] 5.2.1 定义指令类型识别规则（§5.0.2）
    - `复盘`/`总结`/`review` → `createReview` Mutation
    - `查询记忆`/`搜索记忆`/`检索` → `reviews`/`review` Query
    - `更新记忆`/`修改记忆`/`补充` → `updateReview` Mutation
    - `归档记忆`/`删除记忆` → `archiveReview` Mutation
  - [ ] 5.2.2 实现自然语言指令解析逻辑
    - 关键词匹配算法
    - 意图识别优先级（精确匹配 > 模糊匹配 > 上下文推断）
    - 歧义处理策略（AskUserQuestion 机制）
  - [ ] 5.2.3 实现参数提取规范（§5.0.3）
    - `reviewId` 提取：正则匹配 `REV-YYYYMMDD-NNN` 格式
    - `keywords` 提取：分词 + 停用词过滤
    - `taskType` 提取：上下文推断或显式指定
    - 时间表达式解析：`"近三个月"` → ISO 8601 dateFrom
    - 其他参数的默认值设定

- [ ] **Task 5.3: GraphQL Operation 映射模板**
  - [ ] 5.3.1 定义 createReview Mutation 模板
    - 完整的 GraphQL Mutation 语句
    - Variable 定义
    - Payload 字段选择
    - 示例 Variables 值
  - [ ] 5.3.2 定义 reviews Query 模板
    - 多参数查询语句
    - Field Selection 示例
    - Fragment 定义（标准化输出格式）
  - [ ] 5.3.3 定义 updateReview Mutation 模板
    - Partial Update 模式示例
    - 数组追加和字符串覆写的 Variable 构建
  - [ ] 5.3.4 定义 archiveReview Mutation 模板
    - Soft Delete 操作示例
    - 状态变更追踪

- [ ] **Task 5.4: 工具白名单策略实现 (§5.2)**
  - [ ] 5.4.1 定义白名单工具集
    - `Glob`: 文件名模式匹配定位候选集
    - `Grep`: 文件内容关键词搜索初筛
    - `Read`: 读取文件内容（强制 offset/limit）
    - `Write`: 写入/覆盖文件内容
  - [ ] 5.4.2 定义禁止项清单
    - ❌ 任何 Shell 命令（RunCommand 等）
    - ❌ 任何未在白名单中的工具
    - ❌ 文件系统遍历（LS 大目录列举）
  - [ ] 5.4.3 实现工具使用规范
    - 每个工具的使用场景说明
    - 必须参数和可选参数说明
    - 使用示例和反例

- [ ] **Task 5.5: Sequential Resolver Pipeline 流程定义 (§5.3)**
  - [ ] 5.5.1 定义 6 阶段流水线
    - Phase 1: Parse（解析）- 自然语言指令 → GraphQL AST
    - Phase 2: Validate（验证）- AST 通过 GraphQL Schema Validation
    - Phase 3: Locate（定位）- Glob/Grep 快速定位目标文件
    - Phase 4: Execute（执行）- 针对性读取具体内容
    - Phase 5: Persist（持久化）- Write 覆盖写回
    - Phase 6: Return（返回）- Field Selection 精确返回
  - [ ] 5.5.2 定义每个阶段的输入输出契约
    - 输入数据格式
    - 输出数据格式
    - 异常处理策略
  - [ ] 5.5.3 定义阶段间数据传递协议
    - 中间数据结构定义
    - 序列化/反序列化规则

- [ ] **Task 5.6: 错误处理机制实现 (§6.2)**
  - [ ] 5.6.1 定义 5 大错误码体系
    - `E_CMD_INVALID` (400): 指令无法解析或缺少必要参数
    - `E_STORAGE_UNAVAILABLE` (503): 存储目录不存在或无权限访问
    - `E_NOT_FOUND` (404): 查询或更新的 reviewId 不存在
    - `E_SCHEMA_MISMATCH` (422): 结构损坏或 Schema 版本不兼容
    - `E_WRITE_CONFLICT` (409): 写入冲突或并发编辑
  - [ ] 5.6.2 实现标准 GraphQL 错误响应格式
    - `errors[]` 数组结构
    - `message` 字段格式：`E_CODE | 描述`
    - `extensions` 对象：`code`, `hint`, `reviewId` 等
  - [ ] 5.6.3 实现每个错误码的处理逻辑
    - 触发条件判断
    - 用户友好提示生成
    - 恢复建议（hint 字段）
  - [ ] 5.6.4 实现错误恢复策略
    - 可重试错误的自动重试机制
    - 不可重试错误的优雅降级
    - 错误日志记录

- [ ] **Task 5.7: 输出契约定义 (Field Selection Philosophy)**
  - [ ] 5.7.1 定义查询场景输出规范
    - 最大返回数量：Top N=3
    - Fragment 格式：`[reviewId] | 核心结论：{coreConclusion} | 行动：{actionItems[0]}`
    - 每条记录 ≤ 2 行
  - [ ] 5.7.2 定义变更场景输出规范
    - 仅返回 Payload 关键字段：`{ review { reviewId status }, changeSummary }`
    - Diff 输出格式（仅显示变更部分）
  - [ ] 5.7.3 定义通用禁令
    - ❌ 禁止复述用户指令
    - ❌ 禁止过渡性语句（"我帮您查询了..."、"以下是..."）
    - ❌ 禁止礼貌性废话
    - ❌ 禁止完整 Object 展开

- [ ] **Task 5.8: 复盘分析引擎 Prompt 设计 (§3.2)**
  - [ ] 5.8.1 定义四维解析模型 Prompt
    - 维度 1: 背景溯源（任务意图 → 痛点 → 验收标准）
    - 维度 2: 决策链路树（技术选型 → 权衡考量 → 否决方案）
    - 维度 3: 红黑榜总结（成功因素 → 失败教训 → 根因分析）
    - 维度 4: 复用价值判定（通用性 → SOP → 场景标签）
  - [ ] 5.8.2 定义分析引擎执行流程 Prompt
    - 输入解析与验证步骤
    - 中间结果生成（GraphQL Variable 格式）
    - Schema 映射与序列化步骤
    - Mutation 执行与持久化步骤
  - [ ] 5.8.3 定义 AskUserQuestion 补充机制
    - 触发条件：缺少关键信息时
    - 问题设计：封闭式问题优先
    - 回答解析：结构化提取

- [ ] **Task 5.9: 向后兼容性与演进策略 (§6.3)**
  - [ ] 5.9.1 定义 Additive Changes 策略
    - 允许的操作：新增字段、新增 Arguments、新增 Enum Values
    - 禁止的操作：删除/重名字段、修改 Required Field 类型
  - [ ] 5.9.2 定义 @deprecated 三阶段渐进弃用
    - T-N: 标记 `@deprecated(reason: "...")`
    - T-N+1: 强烈建议迁移，Introspection 高亮警告
    - T-N+2: 移除字段，查询返回 null
  - [ ] 5.9.3 定义 Schema 版本迁移指南
    - 版本号语义化（MAJOR.MINOR.PATCH）
    - 迁移检测机制（schemaVersion 字段）
    - 迁移脚本调用方式

- [ ] **Task 5.10: SKILL.md 完整性与质量检查**
  - [ ] 5.10.1 验证总行数 < 500 行
    - 统计当前行数
    - 如超出则精简冗余内容
  - [ ] 5.10.2 验证所有 Section 完整性
    - 对照 spec.md §5.0 检查覆盖度
    - 确保无遗漏的关键功能点
  - [ ] 5.10.3 验证与 schema.graphql 的一致性
    - 所有引用的类型名、字段名与 Schema 一致
    - 所有枚举值与 Schema 定义一致
  - [ ] 5.10.4 验证指令解析准确性
    - 测试 4 种指令类型的识别准确率
    - 测试边界情况（歧义指令、错误指令等）

---

# Phase 6: 核心功能实现 (§3.2-3.5)

> **目标**: 实现复盘分析引擎、检索引擎、更新归档、图关系等核心业务逻辑
> **产出物**: SKILL.md 中的核心逻辑实现（Prompt 层）+ scripts/ 下的辅助脚本
> **质量门禁**: QG-04

- [ ] **Task 6.1: 复盘分析引擎实现 (Review Analysis Engine, §3.2)**
  - [ ] 6.1.1 实现输入解析与验证模块
    - 自然语言输入解析函数
    - 必要参数完整性检查
    - AskUserQuestion 补充机制
  - [ ] 6.1.2 实现四维解析模型
    - 维度 1: 背景溯源解析器
      - 任务意图识别
      - 痛点提取
      - 验收标准确定
    - 维度 2: 决策链路树构建器
      - 技术选型识别
      - 权衡考量梳理
      - 否决方案记录
    - 维度 3: 红黑榜总结生成器
      - 成功因素提炼（红榜）
      - 失败教训识别（黑榜）
      - 根因分析引擎
    - 维度 4: 复用价值判定器
      - 通用性评估
      - SOP 筛选
      - 场景标签标记
  - [ ] 6.1.3 实现 GraphQL Variable 对象生成
    - 中间结果 → CreateReviewInput 映射
    - reviewId 自动生成（REV-YYYYMMDD-NNN 格式，当日递增序号）
    - timestamp 自动设置（ISO 8601 当前时间）
    - 默认值设置（status=ACTIVE, schemaVersion="1.2"）
  - [ ] 6.1.4 实现 createReview Mutation 执行流程
    - Mutation 语句构建
    - 变量绑定
    - 执行与结果处理
    - MyST Markdown 文件写入
    - 极简结果返回（≤10 行）

- [ ] **Task 6.2: 记忆检索引擎实现 (Memory Query & Retrieval, §3.3)**
  - [ ] 6.2.1 实现三阶段检索管道 (Resolver Pipeline)
    - Phase 1: 候选集生成
      - Glob(".storage/reviews/REV-*.md") 文件定位
      - DataLoader batching 优化
    - Phase 2: 关键词初筛
      - Grep 多关键词 OR 逻辑过滤
      - @filter directive 类比实现
    - Phase 3: 精准读取排序
      - Read(top 3, max 120 lines)
      - 相关度评分计算
      - 结果排序与截断
  - [ ] 6.2.2 实现相关度评分因子
    - 因子 1: 关键词命中数量（主要因子，权重 40%）
    - 因子 2: 时间新鲜度（权重 20%）
    - 因子 3: status=ACTIVE 优先（权重 15%）
    - 因子 4: 任务类型匹配（权重 15%）
    - 因子 5: 标签匹配（权重 10%）
  - [ ] 6.2.3 实现查询参数解析
    - keywords: 分词提取
    - taskType: 枚举映射
    - dateFrom/dateTo: 时间表达式解析
    - projectId: 直接提取
    - limit: 默认 3，Hard Limit
  - [ ] 6.2.4 实现查询结果格式化
    - Fragment 格式输出
    - Top 3 截断处理
    - 超出阈值提示消息（§3.3 Scenario: 查询阈值溢出处理）

- [ ] **Task 6.3: 记忆更新与归档实现 (Memory Maintenance, §3.4)**
  - [ ] 6.3.1 实现字段级更新操作 (updateReview Mutation)
    - 数组追加操作（decisionsAppend, successFactorsAppend, failureReasonsAppend, bestPracticesAppend, actionItemsAppend）
    - 字符串覆写操作（taskTypeOverride, statusOverride, issueUrlOverride, prUrlOverride）
    - Partial Update Pattern 实现
  - [ ] 6.3.2 实现归档操作 (archiveReview Mutation)
    - Soft Delete 语义（ACTIVE → ARCHIVED）
    - 状态变更前快照保存（previousStatus）
    - 归档文件移动至 `_archive/` 目录（可选）
  - [ ] 6.3.3 实现极简 Diff 输出生成
    - 变更字段识别
    - Diff 格式化：`📝 变更：{field}: [新增/修改/删除] {content}`
    - changeSummary 生成
  - [ ] 6.3.4 实现并发冲突检测（Optimistic Concurrency Control）
    - Git 冲突标记检测
    - 文件锁机制（如适用）
    - WRITE_CONFLICT 错误返回

- [ ] **Task 6.4: 图关系建模与追溯实现 (Graph Relationships, §3.5)**
  - [ ] 6.4.1 实现向上追溯能力
    - issueUrl 解析与验证（GitHub/GitLab/AtomGit Issues URL 格式）
    - prUrl 解析与验证（GitHub/GitLab/AtomGit PR/MR URL 格式）
    - URL 格式正则表达式定义
    - URL 可点击性验证
  - [ ] 6.4.2 实现向下穿透能力（Issue Comment 回写）
    - Issue Tracker API 调用封装
    - 评论格式标准实现（§7.3 评论格式标准）
    - Fallback Chain：字段 → PR描述 → linked_issues API
  - [ ] 6.4.3 实现横向关联能力
    - 关键词关联检索
    - relatedTo Edge 概念实现
    - Review ↔ Review 语义关联

- [ ] **Task 6.5: Schema Mapping Layer 实现 (§3.6)**
  - [ ] 6.5.1 实现查询到检索的映射流程
    - 用户指令 → 参数提取 → GraphQL Query 构建 → Resolver Pipeline 执行 → Field Selection 输出
    - 完整数据流转链路实现
  - [ ] 6.5.2 实现写入到持久化的映射流程
    - 用户指令 → 分析引擎 → GraphQL Mutation → Resolver 执行 → MyST 写入 → 校验 → 返回
    - 完整数据流转链路实现
  - [ ] 6.5.3 实现映射层与 Resolver 的协调
    - 明确职责边界
    - 数据传递协议
    - 错误传播机制

- [ ] **Task 6.6: 核心功能集成测试**
  - [ ] 6.6.1 测试 createReview 完整流程
    - 输入：复杂上下文描述
    - 验证：GraphQL Schema 合规 + reviewId 格式正确 + 返回 ≤10 行
  - [ ] 6.6.2 测试 reviews 多条件查询
    - 输入：关键词+时间+类型组合
    - 验证：Top 3 返回 + 每条 ≤2 行 + 相关度排序合理
  - [ ] 6.6.3 测试 updateReview 字段级更新
    - 输入：reviewId + 数组追加 + 字符串覆写
    - 验证：Diff 输出正确 + Schema 完整性保持
  - [ ] 6.6.4 测试 archiveReview 归档操作
    - 输入：reviewId
    - 验证：状态变更 + previousStatus 正确
  - [ ] 6.6.5 测试图关系追溯
    - 输入：含 URL 的记录
    - 验证：URL 格式验证 + 关联查询正确

---

# Phase 7: Token 优化控制器 (§6.1)

> **目标**: 实现极致的 Token 优化策略，确保输入输出在合理范围内
> **产出物**: Token 优化控制逻辑（集成在 SKILL.md 和核心引擎中）
> **质量门禁**: QG-04

- [ ] **Task 7.1: 输入侧优化 (Variable Parsing)**
  - [ ] 7.1.1 实现分段读取策略
    - Read 工具的 offset/limit 参数强制使用
    - Cursor-based Pagination 类比实现
    - 大文件自动分段（每段 ≤ 120 行）
  - [ ] 7.1.2 实现信息过滤策略
    - 低价值上下文丢弃规则
      - 日志堆栈（除非明确要求）
      - 无关闲聊内容
      - 未修改代码片段
    - @skip / @include Directive 类比实现
    - 上下文重要性评分模型

- [ ] **Task 7.2: 存储侧优化 (Schema Design Best Practices)**
  - [ ] 7.2.1 实现扁平化结构验证
    - 检测并拒绝过度嵌套的数据结构
    - 推荐格式：`tags: ["react", "frontend"]`
    - 禁止格式：`metadata: { tags: { categories: [...] } }`
  - [ ] 7.2.2 实现信息提纯验证
    - Scalar 值精炼程度检查
    - 推荐格式：`"所有对外服务调用必须设置超时和重试"`
    - 禁止格式：`"我们在测试中发现当外部服务响应超过30秒时..."`
  - [ ] 7.2.3 实现类型安全验证
    - 枚举值使用检查（vs 自由字符串）
    - 标量格式合规性检查

- [ ] **Task 7.3: 输出侧优化 (Response Shape Control)**
  - [ ] 7.3.1 实现查询场景输出控制
    - 最大返回数量限制：N=3（硬阈值）
    - Fragment 格式强制执行
    - 每条记录最大行数：2 行
    - FORBIDDEN 规则 enforcement
      - 禁止完整 Object 展开
      - 禁止整段原文
      - 禁止未请求字段
  - [ ] 7.3.2 实现变更场景输出控制
    - 仅返回 Payload 关键字段
    - Diff-only 输出（Mutation 场景）
    - 禁止完整文件内容返回
    - 禁止未变更字段返回
  - [ ] 7.3.3 实现通用禁令 enforcement
    - 指令复述检测与阻止
    - 过渡性语句检测与阻止
    - 礼貌性废话检测与阻止

- [ ] **Task 7.4: 读取硬阈值控制 (Pagination Limits, §6.1.4)**
  - [ ] 7.4.1 实现最大返回节点数限制
    - Hard Limit: 3 个 Review 节点
    - 类比 GraphQL Connection: `first: Int = 3`
    - 超出时提示用户缩小查询条件
  - [ ] 7.4.2 实现每节点最大行数限制
    - Hard Limit: 120 行/节点
    - Custom Scalar limit 类比
    - 超出时要求用户提供更精确条件
  - [ ] 7.4.3 实现阈值溢出处理
    - 溢出检测逻辑
    - 用户友好提示消息生成
    - 建议优化查询条件的具体方法

- [ ] **Task 7.5: Token 消耗监控与报告**
  - [ ] 7.5.1 实现 Token 使用估算
    - 输入 Token 估算（基于字符数/Token 比例）
    - 输出 Token 估算
    - 总消耗统计
  - [ ] 7.5.2 实现效率指标跟踪
    - 信息密度比（有用信息 / 总 Token）
    - 压缩率（原始内容 / 优化后内容）
  - [ ] 7.5.3 实现优化建议生成
    - 基于历史数据的优化建议
    - 异常消耗预警

---

# Phase 8: CI/CD 工作流与自动化闭环 (§7)

> **目标**: 创建 GitHub Actions 工作流和 Issue 回写机制，实现自动化闭环
> **产出物**: `.github/workflows/auto-review.yml`, `scripts/` 下的自动化脚本
> **质量门禁**: QG-05

- [ ] **Task 8.1: GitHub Actions 工作流配置**
  - [ ] 8.1.1 创建工作流文件 `.github/workflows/auto-review.yml`
  - [ ] 8.1.2 配置触发器（§7.2）
    - GitHub: `pull_request: types: [closed]`, branches: [main, master]
    - GitLab: `merge_request: type: merged`, target_branch: [main, master]
  - [ ] 8.1.3 实现优先级处理规则
    - 🔴 高优先级：`bug`, `architecture` label → 立即执行 + Full Review Mode + Issue 回写
    - 🟡 中优先级：`feature`, `refactor`, `hotfix` label → 延迟 5 分钟 + Standard Review Mode + 可选回写
    - 🟢 低优先级：其他类型 → 每小时批量 + Summary Only Mode + 不回写
  - [ ] 8.1.4 配置环境变量（§7.2 表格）
    - `GITHUB_TOKEN` (Secret, 必需)
    - `LLM_API_KEY` (Secret, 必需)
    - `LLM_API_URL` (Config, 必需)
    - `LLM_MODEL_ID` (Config, 必需)
    - `MEMORY_ROOT` (Config, 可选, 默认 `.storage/`)
    - `WORKFLOW_TIMEOUT` (Config, 可选, 默认 600秒)
    - `LOG_LEVEL` (Config, 可选, 默认 `INFO`)
    - `NOTIFICATION_WEBHOOK` (Secret, 可选)
  - [ ] 8.1.5 配置超时控制（§7.2 表格）
    - 整体工作流：10 分钟
    - 数据收集阶段：120 秒
    - LLM 处理阶段：300 秒
    - 存储写入阶段：30 秒
    - Issue 回写阶段：60 秒

- [ ] **Task 8.2: 数据收集模块 (scripts/data_collector.py)**
  - [ ] 8.2.1 实现 PR/MR 数据获取
    - GitHub/GitLab/AtomGit API 调用封装
    - PR/MR 元信息提取（标题、描述、作者、标签）
    - Code Review 评论收集
    - Diff 内容提取
  - [ ] 8.2.2 实现 Issue 数据获取
    - linked_issues API 调用
    - Issue 元信息提取
    - Issue 评论历史收集
  - [ ] 8.2.3 实现数据聚合与预处理
    - 数据去重与清洗
    - 结构化数据组装
    - 输出为 LLM 处理模块可用的格式

- [ ] **Task 8.3: LLM 处理模块 (scripts/llm_processor.py)**
  - [ ] 8.3.1 实现 LLM API 调用封装
    - 支持多种 LLM Provider（OpenAI 兼容 API）
    - 请求构建与发送
    - 响应解析与错误处理
  - [ ] 8.3.2 实现 GraphQL Mapping 逻辑
    - LLM 输出 → CreateReviewInput 结构映射
    - 四维分析模型 Prompt 应用
    - 结构化结果验证
  - [ ] 8.3.3 实现三种 Review Mode
    - Full Review Mode: 完整四维分析
    - Standard Review Mode: 核心要点提取
    - Summary Only Mode: 一句话总结

- [ ] **Task 8.4: 存储管理模块 (scripts/storage_manager.py)**
  - [ ] 8.4.1 实现 MyST Markdown 文件写入
    - 基于模板生成文件内容
    - 文件命名规范遵循（REV-{PR/MR}-{DATE}.md）
    - 写入至 `.storage/reviews/` 目录
  - [ ] 8.4.2 实现文件读取与更新
    - 已有记录的追加更新
    - Schema 合规性校验集成
  - [ ] 8.4.3 实现存储目录管理
    - 自动创建缺失目录
    - 文件权限设置
    - 备份机制（可选）

- [ ] **Task 8.5: Issue 回写机制 (§7.3)**
  - [ ] 8.5.1 实现 Issue 数据提取（Phase 1）
    - 从 MyST Markdown 提取 reviewId
    - 提取 coreConclusion（≤150 字符）
    - Fallback Chain 实现：字段 → PR描述 → linked_issues API
  - [ ] 8.5.2 实现 Issue 定位（Phase 2）
    - Issue Tracker API 调用
    - 原始 Issue 定位逻辑
  - [ ] 8.5.3 实现评论写入（Phase 3）
    - 标准评论格式生成（§7.3 评论格式标准）
    - Issue Comment API 调用
    - 评论内容：reviewId + 核心结论 + 详情链接
  - [ ] 8.5.4 实现容错与重试机制（§7.3 表格）
    - 401/403: 立即终止 + 通知
    - 404: Warn 日志 + 跳过
    - 429: 指数退避重试（最多 5 次）
    - 5xx: 固定间隔重试（最多 3 次）
    - 网络超时: 重试（最多 3 次，每次 30s）

- [ ] **Task 8.6: 辅助脚本实现**
  - [ ] 8.6.1 实现 `scripts/auto_review_pipeline.py`（主流程编排）
    - 协调各模块执行顺序
    - 错误处理与恢复
    - 状态报告生成
  - [ ] 8.6.2 实现 `scripts/issue_extractor.py`（Issue 数据提取）
    - Issue 元信息解析
    - 关联 PR/MR 识别
  - [ ] 8.6.3 实现 `scripts/issue_writer.py`（Issue 评论写入）
    - API 调用封装
    - 格式验证
  - [ ] 8.6.4 实现 `scripts/retry_handler.py`（容错与重试）
    - 通用重试逻辑
    - 退避策略实现
    - 重试次数限制
  - [ ] 8.6.5 实现 `scripts/logger.py`（日志记录）
    - 结构化日志格式
    - 多级别日志支持
    - 日志轮转（可选）
  - [ ] 8.6.6 实现 `scripts/notifier.py`（失败通知）
    - Webhook 调用封装
    - 通知模板
    - 发送频率限制

- [ ] **Task 8.7: 双向追溯性保障 (§7.4)**
  - [ ] 8.7.1 实现向上追溯验证
    - 复盘记录 → PR/MR 页面链接验证
    - prUrl 可点击跳转测试
  - [ ] 8.7.2 实现向下穿透验证
    - Issue → 复盘评论回写验证
    - reviewId 和核心结论正确性
  - [ ] 8.7.3 实现横向关联验证
    - 关键词 → 相关记录检索验证
    - GraphQL Query 正确性

---

# Phase 9: 上下文注入系统 (§8)

> **目标**: 创建 IDE 插件体系，实现防错预警和无感挂载功能
> **产出物**: `plugins/` 下的 IDE 插件模块
> **质量门禁**: QG-05（响应时间 ≤ 300ms）

- [ ] **Task 9.1: IDE 插件架构设计**
  - [ ] 9.1.1 定义插件管理器 (plugins/plugin_manager.py)
    - 插件生命周期管理（加载、初始化、卸载）
    - 插件注册表
    - 事件总线
  - [ ] 9.1.2 定义插件接口规范
    - 标准插件接口（IPlugin）
    - 事件监听器接口
    - 数据提供者接口
  - [ ] 9.1.3 实现插件加载与配置
    - 配置文件解析
    - 依赖注入
    - 错误隔离（单个插件失败不影响其他插件）

- [ ] **Task 9.2: 防错预警模块 (plugins/failure_detector.py, §8.2)**
  - [ ] 9.2.1 实现文件事件监听器
    - 文件打开事件捕获
    - 文件保存事件捕获
    - 文件切换事件捕获
  - [ ] 9.2.2 实现检测算法流程（§8.2 Step 1-4）
    - Step 1: 路径匹配 → 提取文件名和模块路径作为 keywords
    - Step 2: 故障标签过滤 → 过滤 bug/incident/crash 标签记录
    - Step 3: 关联路径匹配 → 精确 + 模糊匹配
    - Step 4: 风险评分计算 → 多因子加权模型
  - [ ] 9.2.3 实现风险评分模型（§8.2 表格）
    - 因子 1: 故障记录数量（权重 40%）
    - 因子 2: 故障严重程度（权重 25%）
    - 因子 3: 时间新鲜度（权重 20%）
    - 因子 4: 复现频率（权重 15%）
    - 综合评分计算
  - [ ] 9.2.4 实现风险等级判定
    - 🟢 低风险：score < 30 → 无提示
    - 🟡 中风险：30 ≤ score < 60 → Info 级别提示
    - 🔴 高风险：score ≥ 60 → Warning 级别 + 详细建议
  - [ ] 9.2.5 实现提示格式化输出（§8.2 提示格式示例）
    - 标准提示模板
    - 推荐最佳实践列表
    - 详情查看指引（@skill 查询记忆 ...）

- [ ] **Task 9.3: 无感挂载模块 (plugins/smart_query_engine.py 等, §8.3)**
  - [ ] 9.3.1 实现 Prompt 意图分析器 (plugins/intent_analyzer.py)
    - 关键词提取（技术领域 + 模块名 + 操作类型）
    - 任务类型识别（CRUD/API/UI/Algorithm/Infrastructure）
    - 复杂度估算（Simple/Medium/Complex）
  - [ ] 9.3.2 实现隐式 GraphQL Query 构建器 (plugins/smart_query_engine.py)
    - Query 变量构建（$keywords, $taskType, $limit: 5）
    - Field Selection（reviewId, coreConclusion, bestPractices）
    - 三阶段检索执行（Glob → Grep → Read）
  - [ ] 9.3.3 实现相关性分析器 (plugins/correlation_analyzer.py)
    - 四维评分模型
      - 关键词匹配（权重 40%）
      - 任务类型匹配（权重 25%）
      - 时间新鲜度（权重 20%）
      - 适用性评估（权重 15%）
    - 硬阈值过滤（relevance_score ≥ 0.85）
    - Top 3 选择
  - [ ] 9.3.4 实现上下文注入器 (plugins/context_injector.py)
    - Best Practices 精简摘要提炼
    - System Prompt 增强片段构建
    - 透明注入到 AI 的 System Prompt
  - [ ] 9.3.5 实现请求拦截器 (plugins/request_interceptor.py)
    - AI 请求拦截
    - 上下文增强逻辑触发
    - 增强后的请求转发

- [ ] **Task 9.4: 提示注入器实现 (plugins/tooltip_injector.py)**
  - [ ] 9.4.1 实现 IDE Tooltip 集成
    - VS Code Extension API 对接
    - Trae IDE Plugin SDK 对接
    - Hover 提示内容渲染
  - [ ] 9.4.2 实现提示内容动态生成
    - 基于风险评估结果的提示内容
    - 基于历史经验的建议内容
    - 可操作的快速链接

- [ ] **Task 9.5: 透明化设计原则实现 (§8.3)**
  - [ ] 9.5.1 实现无感注入
    - 后台并行执行（≤300ms）
    - 零延迟感知
    - 用户无感知
  - [ ] 9.5.2 实现可覆盖机制
    - "忽略历史经验" 指令检测
    - 注入禁用开关
    - 会话级配置
  - [ ] 9.5.3 实现可追溯性
    - 每条注入内容包含来源 reviewId
    - 注入日志记录
    - 来源链接可点击
  - [ ] 9.5.4 实现非侵入式注入
    - 附加在 System Prompt 末尾
    - 不修改原始 Prompt
    - 清晰的分隔标记

- [ ] **Task 9.6: 性能优化与监控**
  - [ ] 9.6.1 实现性能指标达标（§8.2 性能要求表格）
    - 插件加载时间 ≤ 500ms
    - 文件检测响应时间 ≤ 300ms
    - 内存占用 ≤ 50MB
    - CPU 占用 ≤ 5%
  - [ ] 9.6.2 实现缓存机制
    - 查询结果缓存
    - 风险评分缓存
    - 缓存失效策略（TTL / 手动刷新）
  - [ ] 9.6.3 实现效果评估指标采集 (plugins/metrics_collector.py)
    - 效率指标（§8.6 效率指标表格）
      - 上下文命中率 ≥ 70%
      - 问题预防率 ≥ 60%
      - 查询加速比 ≥ 1.5x
      - 用户干预减少率 ≥ 50%
    - 质量指标（§8.6 质量指标表格）
      - 代码规范合规率 ≥ 80%
      - 反模式检出率 ≥ 85%
      - 相关性准确率 ≥ 85%
      - 误报率 ≤ 10%

- [ ] **Task 9.7: 数据安全与隐私保护 (§8.5)**
  - [ ] 9.7.1 实现本地存储优先策略
    - 所有数据存储在本地 `.storage/` 和 `.cache/`
    - 远程存储可选配置
  - [ ] 9.7.2 实现敏感信息管理
    - API Key 通过 Keychain 或环境变量管理
    - 禁止明文存储敏感信息
    - 内存中及时清除
  - [ ] 9.7.3 实现审计日志
    - 记录所有数据访问操作
    - 时间戳、操作者、操作类型、对象
    - 日志防篡改（可选）
  - [ ] 9.7.4 实现数据脱敏
    - 日志中敏感字段仅显示前 4 位 + `...`
    - 正则脱敏规则
  - [ ] 9.7.5 实现用户同意机制
    - 首次使用弹出数据使用说明
    - 获得用户确认
    - 选择记录
  - [ ] 9.7.6 实现一键清除功能
    - 清除所有本地缓存
    - 清除历史数据
    - 确认对话框

- [ ] **Task 9.8: IDE 兼容性矩阵实现 (§8.4)**
  - [ ] 9.8.1 实现 VS Code 完整支持
    - Extension API 集成
    - 防错预警 + 无感挂载
  - [ ] 9.8.2 实现 Trae IDE 完整支持
    - Plugin SDK 集成
    - 全功能支持
  - [ ] 9.8.3 实现 JetBrains IDEA 部分支持
    - IntelliJ Platform Plugin
    - 核心功能适配
  - [ ] 9.8.4 实现 Vim/Neovim 实验支持
    - LSP Client + autocmd
    - 基础功能
  - [ ] 9.8.5 实现 Cursor/Windsurf 兼容
    - VS Code API 兼容层
    - 完整功能

---

# Phase 10: 记忆生命周期管理与知识图谱 (§9)

> **目标**: 实现记忆衰减检测、归档管理和知识图谱构建功能
> **产出物**: 归档脚本、知识图谱构建工具
> **质量门禁**: QG-05

- [ ] **Task 10.1: 生命周期元数据扩展 (§9.2 GraphQL Type Definition)**
  - [ ] 10.1.1 在 `schema.graphql` 中扩展 LifecycleMetadata 类型
    - `lastAccessedAt: DateTime`
    - `accessCount: Int!`
    - `accessFrequency30d: Int!`
    - `accessFrequency90d: Int!`
    - `accessTrend: AccessTrend!` (RISING/STABLE/DECLINING)
    - `creationAgeDays: Int!`
    - `category: LifecycleCategory!` (ARCHITECTURE/SECURITY/BUSINESS_LOGIC/UI_FRONTEND/DATA_MODEL/INCIDENT)
    - `importanceScore: Float!` (0.0 - 1.0)
    - `decayIndicator: Boolean!`
    - `archiveRecommendation: ArchiveRecommendation` (STRONGLY_RECOMMENDED/RECOMMENDED/NOT_RECOMMENDED)
    - `archivedAt: DateTime`
    - `archivedReason: String`
  - [ ] 10.1.2 定义 AccessTrend 枚举
  - [ ] 10.1.3 定义 LifecycleCategory 枚举
  - [ ] 10.1.4 定义 ArchiveRecommendation 枚举
  - [ ] 10.1.5 更新 md_graphql_converter.py 支持新字段
  - [ ] 10.1.6 更新 validate_graphql_schema.py 支持新字段校验

- [ ] **Task 10.2: 记忆衰减检测器实现**
  - [ ] 10.2.1 实现定期巡检脚本
    - 定时触发机制（cron / 手动）
    - 全量扫描 `.storage/reviews/` 目录
  - [ ] 10.2.2 实现衰减检测指标（§9.2 表格）
    - 时间老化检测：`creationAgeDays > 365` → ⚠️ 老化警告
    - 访问停滞检测：距上次访问 > 180天 → 🔴 停滞警告
    - 频率下降检测：`freq30d / freq90d < 0.3` → 📉 衰减趋势
    - 零引用检测：`accessCount = 0` → ❌ 孤岛记录
  - [ ] 10.2.3 实现类别分类与归档策略（§9.2 表格）
    - ARCHITECTURE: ⛔ 禁止自动归档（需人工确认）
    - SECURITY: ⛔ 禁止自动归档（长期保留）
    - BUSINESS_LOGIC: ✅ 可自动归档（低风险）
    - UI_FRONTEND: ✅ 可自动归档（低风险）
    - DATA_MODEL: ⚠️ 需谨慎归档
    - INCIDENT: ⚠️ 需保留较长时间（≥2年）
  - [ ] 10.2.4 实现综合评分公式（§9.2 伪代码）
    - lifecycle_score = 0.35 * importanceScore + 0.25 * activity_score + 0.20 * connectivity_score + 0.20 * timeliness_score
    - 归档判定逻辑：
      - score < 0.30 → STRONGLY_RECOMMENDED
      - 0.30 ≤ score < 0.50 → RECOMMENDED
      - score ≥ 0.50 → NOT_RECOMMENDED

- [ ] **Task 10.3: 归档建议生成器实现**
  - [ ] 10.3.1 实现归档建议报告生成
    - 待归档记录列表
    - 每条记录的评分明细
    - 归档建议理由
  - [ ] 10.3.2 实现人工审核工作流
    - 建议列表展示
    - 批量批准/拒绝操作
    - 单条记录详细审查
  - [ ] 10.3.3 实现自动归档执行（可选）
    - 确认后执行 archiveReview Mutation
    - 文件移动至 `_archive/` 目录
    - 归档日志记录

- [ ] **Task 10.4: 知识图谱实体类型体系实现 (§9.3)**
  - [ ] 10.4.1 在 `schema.graphql` 中定义 GraphEntity Union 类型
    - ModuleEntity
    - ComponentEntity
    - APIEntity
    - DataStructureEntity
    - FunctionEntity
    - TechnologyEntity
    - ConceptEntity
    - IssueTrackerEntity
    - PatternEntity
    - RiskEntity
  - [ ] 10.4.2 定义 GraphNode Interface
    - `id: ID!`
    - 公共字段定义
  - [ ] 10.4.3 实现各实体类型定义
    - ModuleEntity: id, name, description, filePath
    - ComponentEntity: id, name, parentModule, description
    - 其他实体类型类似定义
  - [ ] 10.4.4 定义 GraphRelationType 枚举
    - DEPENDS_ON, CALLS, CONTAINS, USES, RELATED_TO, CAUSES, SOLVED_BY, EVOLVES_TO

- [ ] **Task 10.5: 知识图谱关系类型体系实现 (§9.3)**
  - [ ] 10.5.1 定义 GraphConnection 类型（Connection Pattern）
    - `edges: [GraphEdge!]!`
    - `pageInfo: PageInfo!`
    - `totalCount: Int!`
  - [ ] 10.5.2 定义 GraphEdge 类型
    - `cursor: String!`
    - `node: GraphEntity!`
    - `relationType: GraphRelationType!`
    - `weight: Float`
    - `metadata: GraphQL::JSON`
  - [ ] 10.5.3 实现关系抽取机制
    - 从代码分析中提取实体
    - 从复盘记录中提取关系
    - 自动关系发现算法

- [ ] **Task 10.6: 脆弱点分析模型实现 (§9.3)**
  - [ ] 10.6.1 定义 Vulnerability Analysis Query
    - vulnerabilities(projectId) 查询
    - vulnerabilityScore, riskLevel 字段
    - spofRisk, failureClusterRisk, chainRisk 字段
    - affectedNodes 联合类型
  - [ ] 10.6.2 实现脆弱点评分算法
    - vulnerability_score = 0.40 * spof_risk + 0.35 * failure_cluster_risk + 0.25 * chain_risk
    - RiskLevel 判定：
      - CRITICAL (≥ 0.80): 立即关注
      - HIGH (0.60 - 0.80): 纳入技术债务清单
      - MEDIUM (0.40 - 0.60): 保持监控
      - LOW (< 0.40): 暂不处理
  - [ ] 10.6.3 实现脆弱点报告生成
    - 风险热力图
    - 影响范围分析
    - 修复建议优先级排序

- [ ] **Task 10.7: 知识图谱存储方案选择与实现**
  - [ ] 10.7.1 评估三种存储方案（§9.3 表格）
    - 方案 A: SDL 文件 + Resolver（< 10K 实体）
    - 方案 B: PostgreSQL + pg_graphql（10K-100K）
    - 方案 C: Neo4j + graphql-neo4j（> 100K）
  - [ ] 10.7.2 实现初始方案（方案 A: SDL 文件）
    - 图谱数据文件存储格式
    - Resolver 实现基础查询
    - 图遍历算法基础实现
  - [ ] 10.7.3 实现图谱可视化接口
    - 导出为可视化平台可用格式
    - D3.js / Cytoscape.js 兼容数据格式
    - Web 可视化页面（可选）

- [ ] **Task 10.8: Review Node 与知识图谱集成 (§9.1)**
  - [ ] 10.8.1 实现 Review 作为图谱锚点
    - Review 实现 Node 接口的验证
    - Review → GraphEntity 的映射
  - [ ] 10.8.2 实现向上追溯边
    - issueUrl/prUrl → 外部实体连接
    - URL 解析与实体关联
  - [ ] 10.8.3 实现向下穿透边
    - Issue Comment 回写 → 反向连接
    - 回写记录追踪
  - [ ] 10.8.4 实现横向关联边
    - 关键词关联 → Review ↔ Review 连接
    - relatedTo Edge 概念实现
  - [ ] 10.8.5 实现实体挂载
    - Review 作为 ModuleEntity 元数据
    - 复盘结论挂载到代码模块

---

# Phase 11: 测试用例编写与集成验证 (§10)

> **目标**: 编写全面的测试用例，验证所有功能的正确性和稳定性
> **产出物**: 测试文件、测试报告、集成验证清单
> **质量门禁**: QG-06（测试通过率 ≥ 90%）

- [ ] **Task 11.1: MyST 格式基础测试 (§10.1, 5 个 Test Cases)**
  - [ ] 11.1.1 编写 TC1: 模板生成正确性测试
    - 验证目标：MyST 文件创建与 GraphQL Schema 映射
    - 关键检查点：
      - YAML Front Matter 完整性
      - 5 个 Admonition 存在性
      - 核心结论 ≤150 字符
    - 测试数据：spec.md §4.1.2 完整模板示例
    - 断言：所有检查点 PASS
  - [ ] 11.1.2 编写 TC2: MD → GraphQL 转换测试
    - 验证目标：双向转换准确性
    - 关键检查点：
      - 转换后数据可通过 GraphQL Schema 校验
      - 字段映射正确性（17 个字段逐一验证）
      - 无数据丢失
    - 测试数据：多种 MyST 文件样本
    - 断言：转换准确率 ≥ 98%
  - [ ] 11.1.3 编写 TC3: GraphQL → MD 反向转换测试
    - 验证目标：转换一致性
    - 关键检查点：
      - MD 通过合规校验
      - 语义等价性
      - 字段值一致性
    - 测试数据：多种 GraphQL 对象样本
    - 断言：往返转换一致性 100%
  - [ ] 11.1.4 编写 TC4: GraphQL Schema 合规性校验测试
    - 验证目标：验证脚本准确率
    - 关键检查点：
      - PASS/WARN/FAIL 判定正确性
      - 误判率 ≤ 5%
      - 错误信息可操作性
    - 测试数据：正常/异常/边界 MyST 文件
    - 断言：误判率 ≤ 5%
  - [ ] 11.1.5 编写 TC5: 单格式存储一致性测试
    - 验证目标：端到端验证
    - 关键检查点：
      - 写入 MD → Schema 校验 → 读取 → 再校验流程完整
      - 异常降级正常
    - 测试数据：完整 CRUD 操作序列
    - 断言：端到端流程零错误

- [ ] **Task 11.2: 核心功能测试 (§10.2, 5 个 Test Cases)**
  - [ ] 11.2.1 编写 TC1: 完整复盘流程测试
    - 验证目标：createReview Mutation
    - 输入：复杂上下文描述
    - 验证项：
      - GraphQL Schema 合规
      - reviewId 格式正确（REV-YYYYMMDD-NNN）
      - 返回 ≤10 行
    - 断言：全部验证项 PASS
  - [ ] 11.2.2 编写 TC2: 参数化查询测试
    - 验证目标：reviews Query
    - 输入：关键词+时间+类型组合
    - 验证项：
      - Top 3 返回
      - 每条 ≤2 行
      - 相关度排序合理
    - 断言：排序合理性人工评审通过
  - [ ] 11.2.3 编写 TC3: 字段级更新与归档测试
    - 验证目标：updateReview / archiveReview Mutations
    - 输入：数组追加 + 字符串覆写 + 状态变更
    - 验证项：
      - Diff 输出正确
      - Schema 完整性保持
      - 归档状态正确
    - 断言：变更前后一致性验证通过
  - [ ] 11.2.4 编写 TC4: 图关系追溯测试
    - 验证目标：Graph Traversal
    - 输入：含 URL 的记录创建 + 反向查询
    - 验证项：
      - URL 格式验证
      - 关联 Query 正确
    - 断言：URL 可解析且关联正确
  - [ ] 11.2.5 编写 TC5: 向后兼容性测试
    - 验证目标：Schema Evolution
    - 输入：旧版本记录 + 新版 Schema 读取
    - 验证项：
      - 兼容层映射正确
      - 无报错
      - 数据完整
    - 断言：旧记录正常读取

- [ ] **Task 11.3: 量化断言验证 (§10.3, 15 项 Assertions)**
  - [ ] 11.3.1 GraphQL Schema 合规性断言（5 项）
    - [ ] required_fields_present: 所有 `!` 字段非空
    - [ ] review_id_format_match: ReviewID 正则约束
    - [ ] timestamp_iso8601: DateTime ISO 8601 格式
    - [ ] enum_values_valid: status/taskType 在预定义范围
    - [ ] no_extra_fields: 拒绝 Schema 未定义字段
  - [ ] 11.3.2 输出契约断言（Field Selection, 4 项）
    - [ ] review_output_lines ≤ 10
    - [ ] query_result_per_item ≤ 2
    - [ ] no_full_object_expansion_in_output
    - [ ] diff_only_for_updates
  - [ ] 11.3.3 工具白名单断言（3 项）
    - [ ] only_whitelisted_tools_used
    - [ ] no_shell_commands
    - [ ] read_with_offset_limit
  - [ ] 11.3.4 GraphQL 错误处理断言（3 项）
    - [ ] error_extensions_format_valid
    - [ ] hint_actionable
    - [ ] all_5_error_codes_covered

- [ ] **Task 11.4: 集成测试验证清单 (§10.4, 8 项)**
  - [ ] 11.4.1 验证技能在 Trae IDE 环境中正常加载
    - SKILL.md 解析无误
    - 技能注册成功
    - 指令识别正常
  - [ ] 11.4.2 验证三条 Mutations 和一条 Query 正确触发
    - createReview 触发与执行
    - updateReview 触发与执行
    - archiveReview 触发与执行
    - reviews/review 触发与执行
    - 输出合法且合规
  - [ ] 11.4.3 验证工具白名单约束有效执行
    - 白名单内工具正常使用
    - 白名单外工具调用被阻止
    - 违规检测率 = 0%
  - [ ] 11.4.4 验证跨平台路径处理正确
    - Windows 路径测试
    - macOS/Linux 路径测试
    - 相对路径与绝对路径处理
  - [ ] 11.4.5 验证 Git 协作场景
    - `.storage/` 可 track（纳入版本控制）
    - `.cache/` 被 ignore（加入 .gitignore）
    - 合并冲突处理
  - [ ] 11.4.6 验证与其他技能兼容
    - doc-coauthoring 兼容性
    - pdf 技能兼容性
    - xlsx 技能兼容性
    - 并存运行无冲突
  - [ ] 11.4.7 验证 GraphQL Schema 可通过 Validator 校验
    - `graphql validate` 命令通过
    - 或 `graphqxl` 工具通过
    - 无 Syntax Error 或 Validation Error
  - [ ] 11.4.8 验证 GraphQL Introspection Query 返回正确
    - `__schema` 查询返回完整类型信息
    - `__type` 查询返回字段详情
    - isDeprecated, defaultValue 等元信息正确

- [ ] **Task 11.5: 性能与压力测试**
  - [ ] 11.5.1 大规模数据集测试
    - 100+ 复盘记录的查询性能
    - 批量导入/导出性能
    - 内存占用测试
  - [ ] 11.5.2 并发操作测试
    - 同时多个查询的性能
    - 并发写入的冲突处理
    - 锁竞争与死锁检测
  - [ ] 11.5.3 长时间运行稳定性测试
    - 24 小时连续运行
    - 内存泄漏检测
    - 资源释放验证

- [ ] **Task 11.6: 安全性测试**
  - [ ] 11.6.1 输入注入攻击测试
    - SQL Injection（如适用）
    - XSS（如适用）
    - Command Injection（Shell 命令防范）
    - GraphQL Injection（恶意查询）
  - [ ] 11.6.2 路径遍历攻击测试
    - `../` 路径尝试
    - 绝对路径注入
    - 符号链接攻击
  - [ ] 11.6.3 敏感信息泄露测试
    - API Key 是否出现在日志中
    - 错误信息是否泄露内部细节
    - 调试信息是否在生产环境暴露

- [ ] **Task 11.7: 测试报告生成与交付**
  - [ ] 11.7.1 生成测试执行报告
    - 测试用例总数、通过数、失败数
    - 通过率百分比
    - 失败用例详情
  - [ ] 11.7.2 生成覆盖率报告
    - 代码覆盖率（如适用）
    - 功能覆盖率
    - 需求覆盖率（对照 spec.md）
  - [ ] 11.7.3 生成质量门禁检查报告
    - QG-01 ~ QG-06 各项检查结果
    - 未通过项及原因分析
    - 修复建议
  - [ ] 11.7.4 编写验收结论
    - 总体评估（通过/有条件通过/不通过）
    - 遗留问题清单
    - 上线建议

---

## 📊 任务统计汇总

| Phase | 名称 | 主任务数 | 子任务数 | 预估工作量 | 优先级 |
|-------|------|---------|---------|-----------|--------|
| **1** | GraphQL Schema 定义 | 10 | ~45 | 高 | P0 |
| **2** | MyST ↔ GraphQL 转换器 | 10 | ~38 | 高 | P0 |
| **3** | Schema 合规性校验工具 | 10 | ~32 | 高 | P0 |
| **4** | MyST 标准模板 | 10 | ~28 | 中 | P0 |
| **5** | SKILL.md 主文件 | 10 | ~35 | 高 | P0 |
| **6** | 核心功能实现 | 6 | ~28 | 高 | P0 |
| **7** | Token 优化控制器 | 5 | ~18 | 中 | P1 |
| **8** | CI/CD 工作流 | 7 | ~32 | 中 | P1 |
| **9** | 上下文注入系统 | 8 | ~42 | 中 | P1 |
| **10** | 记忆生命周期与知识图谱 | 8 | ~35 | 低 | P2 |
| **11** | 测试与验证 | 7 | ~32 | 高 | P0 |
| **总计** | **11 Phases** | **91** | **~365** | - | - |

---

## 🎯 里程碑计划 (Milestones)

| 里程碑 | 包含 Phase | 目标 | 验收标准 |
|--------|-----------|------|---------|
| **M1: 基础架构就绪** | Phase 1-4 | Schema、转换器、校验器、模板完成 | QG-01, QG-02, QG-03 通过 |
| **M2: 核心功能可用** | Phase 5-7 | SKILL.md、核心引擎、Token 优化完成 | QG-04 通过，四条操作可独立执行 |
| **M3: 自动化闭环** | Phase 8-10 | CI/CD、上下文注入、生命周期管理完成 | QG-05 通过，自动化流程可触发 |
| **M4: 生产就绪** | Phase 11 | 全面测试验证完成 | QG-06 通过，测试通过率 ≥ 90% |

---

*文档版本*: v1.0
*基于 spec.md*: v3.0 (GraphQL-Native Edition)
*生成时间*: 2026-04-17
