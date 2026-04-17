# Prompt 落地优化（方案 B）设计文档

## 背景
当前仓库已具备：
- 记忆记录结构定义：`src/memory-schema.json`（顶层扁平字段、禁止额外字段）
- System Prompt 初稿：`src/system-prompt.md`（强调 Token 控制与多文件操作顺序）
- Mock 记忆记录：`.storage/reviews/REV-*.json`
- CI 基础校验：JSON 语法校验 + reviews 目录记录校验

但仍存在两类关键风险：
- 工具约束表述不一致（例如出现非白名单工具名），导致执行歧义与不可控行为
- “复盘写入/查询”的输出契约仅强调“极简”，缺少可验收的必须返回/禁止返回模板，易造成 Token 浪费或信息泄露（输出完整 JSON）

## 目标
在不引入额外 MCP Server 与复杂依赖的前提下，通过对 `src/system-prompt.md` 的落地优化，完成以下目标：
- 明确且一致的工具白名单与多文件操作顺序
- 复盘写入与查询的输出契约可验收（必须返回/禁止返回）
- 将写入数据与 `src/memory-schema.json` 的 required 字段严格对齐
- 通过硬阈值限制读取范围与返回规模，降低 Token 消耗

## 范围
### In Scope
- 仅修改 `src/system-prompt.md` 的文本规范与模板（不改代码逻辑）
- 强制覆盖两类场景：复盘写入、查询
- 对存储路径、命名、字段默认值给出明确约定

### Out of Scope
- 更新/归档流程的模板与约束（后续迭代补齐）
- 引入 `jsonschema` 等第三方库或 MCP 工具
- 改动 `src/memory-schema.json`（当前以稳定为优先）

## 方案（方案 B：契约分区）
在 `src/system-prompt.md` 中新增一个 “Contract” 区块，用于集中定义规则；原有 Workflow 保留，但引用 Contract 的强约束。

### 1) 工具白名单（强约束）
仅允许调用：
- `Glob`
- `Grep`
- `Read`
- `Write`

禁止调用：
- `LS`
- 任意 Shell 命令
- 任意未在白名单中的工具名（包括但不限于 `SearchReplace`）

### 2) 存储契约（强约束）
写入目录固定：
- `.storage/reviews/`

文件名与 `review_id` 规则：
- `REV-YYYYMMDD-NNN.json`
- `review_id` 必须匹配 `^REV-[0-9]{8}-[0-9]{3}$`

字段对齐 `src/memory-schema.json`：
- required 字段必须齐全：`review_id`、`timestamp`、`participants`、`task_type`、`decisions`、`success_factors`、`failure_reasons`、`best_practices`、`action_items`、`status`
- `timestamp` 必须为 ISO8601 date-time（示例：`2026-04-17T08:24:00Z`）
- 数组字段缺失时必须写入 `[]`
- `status` 默认 `active`（仅允许 `active|archived`）
- 禁止额外字段（与 schema 的 `additionalProperties: false` 对齐）

### 3) 复盘写入（Workflow + 输出契约）
#### Workflow
1. 从输入上下文中提取 required 字段内容
2. 生成符合 schema 的 JSON 记录
3. 写入 `.storage/reviews/REV-YYYYMMDD-NNN.json`
4. 仅返回极简写入结果

#### 输出模板（必须返回/禁止返回）
必须返回：
- 仅返回 `review_id`
- 可选追加一行 file path（不包含 JSON 内容）

禁止返回：
- 在聊天中输出完整 JSON
- 在聊天中输出超过 10 行的复盘详情

### 4) 查询（Workflow + 输出契约）
#### Workflow
1. `Glob` 定位候选：`.storage/reviews/REV-*.json`
2. `Grep` 关键词初筛（必要时分多个关键词）
3. `Read` 少量命中文件片段（按硬阈值限制）
4. 组装极简结果返回

#### 读取硬阈值
- 最多读取 3 个文件
- 每个文件最多读取 120 行片段（必要时使用 `offset/limit`）
- 超出阈值必须要求用户补充更精确的查询条件

#### 返回模板（默认 Top N=3）
必须返回：
- 最多返回 3 条命中
- 每条命中仅包含：`review_id` + 1 句结论 + 1 条最关键 `action_items`（若无则返回 “无”）

禁止返回：
- 输出完整 JSON
- 输出整段原文/整份复盘报告

## 验收标准
- `src/system-prompt.md` 中不出现任何非白名单工具名
- 对“复盘写入/查询”各自存在清晰的必须返回/禁止返回模板
- 对写入的数据约束能够逐条映射到 `src/memory-schema.json` 的 required 字段与枚举约束
- 对查询存在可执行的“Glob + Grep + Read”流程与明确硬阈值

## 变更清单（预期修改点）
- `src/system-prompt.md`
  - 新增 “Contract” 区块（工具白名单、存储契约、写入/查询输出模板、读取阈值）
  - 移除或改写任何非白名单工具的描述
