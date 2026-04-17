# Prompt Contract (Write & Query) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `src/system-prompt.md` 中落地“Contract”分区，强制约束工具白名单与复盘写入/查询的极简输出模板，确保与 `src/memory-schema.json` 契约一致并降低 Token 消耗。

**Architecture:** 仅修改 Prompt 文本，不引入新依赖与新运行时能力；通过“Contract”集中定义工具白名单、存储命名、读写阈值、输出模板与禁止项，原 Workflow 仅引用 Contract 的规则以保持结构清晰。

**Tech Stack:** Markdown（System Prompt 文本）、GitHub Actions（已存在）、Python（仅用于本地/CI 校验脚本，已存在）。

---

## File Structure

- Modify: `src/system-prompt.md`
  - 新增 `# Contract` 区块（工具白名单、存储契约、写入/查询的模板与禁止项、读取阈值）
  - 移除或改写任何非白名单工具的描述（尤其 `SearchReplace`、`LS`）
  - 保持现有“Role/Core Capabilities/Workflow”等章节，但让 Workflow 明确“以 Contract 为准”
- Reference (read-only): `src/memory-schema.json`
  - required 字段清单与约束（`additionalProperties: false`、`status` enum）
- Optional (not required for MVP): `review_memory_skill_spec.md`
  - 该文档包含旧 schema 示例（`system_meta/metadata/...`），本计划不修改它，但后续迭代可补“schema 已扁平化”的勘误说明

## Task 1: Add Contract section to system prompt

**Files:**
- Modify: `src/system-prompt.md`

- [ ] **Step 1: Read current prompt and locate insertion point**

Read: `src/system-prompt.md`  
目标：确认 Prompt 主体是否被包裹在 ```markdown 代码块内，并选择插入 `# Contract` 的位置（推荐放在 `# Workflow` 之后、`# Multi-File Operations Guidelines` 之前）。

- [ ] **Step 2: Add Contract section (exact content)**

在 Prompt 主体中插入以下区块（按现有中文风格保留加粗/列表风格）：

```markdown
# Contract (Strict)
以下规则为强约束。若与其他段落冲突，以本段为准。

## Allowed Tools (Whitelist)
仅允许使用：`Glob`、`Grep`、`Read`、`Write`
禁止使用：`LS`、任何 Shell 命令、以及任何未在白名单中的工具名（包括但不限于 `SearchReplace`）

## Storage Contract
- Root: `.storage/reviews/`
- File & ID: `REV-YYYYMMDD-NNN.json` 且 `review_id` 必须匹配 `^REV-[0-9]{8}-[0-9]{3}$`
- Schema: 必须严格满足 `src/memory-schema.json`
  - required: `review_id`, `timestamp`, `participants`, `task_type`, `decisions`, `success_factors`, `failure_reasons`, `best_practices`, `action_items`, `status`
  - `timestamp`: ISO 8601 date-time（例：`2026-04-17T08:24:00Z`）
  - 数组字段缺失必须写 `[]`
  - `status`: 仅允许 `active|archived`，默认 `active`
  - 禁止额外字段（`additionalProperties=false`）

## Write (Retrospective) Output Contract
写入成功后聊天返回必须满足：
- MUST: 仅返回 `review_id`
- OPTIONAL: 可追加 1 行 file path（不包含 JSON 内容）
- FORBIDDEN: 输出完整 JSON；输出超过 10 行的复盘详情

## Query Output Contract (Top N=3)
查询结果返回必须满足：
- MUST: 最多返回 3 条命中
- MUST: 每条仅包含 `review_id` + 1 句核心结论 + 1 条最关键 `action_items`（若无则为 “无”）
- FORBIDDEN: 输出完整 JSON；输出整段原文/整份复盘报告

## Query Workflow (Token Limits)
- 先 `Glob` 定位候选：`.storage/reviews/REV-*.json`
- 再 `Grep` 初筛关键词
- 后 `Read` 少量命中文件片段
- Hard Limits: 最多读取 3 个文件；每个文件最多读取 120 行片段（必要时使用 `offset/limit`）
- 超出阈值：必须要求用户补充更精确的查询条件
```

- [ ] **Step 3: Remove/replace non-whitelisted tool mentions**

将现有 Prompt 中以下表述替换为白名单一致版本：
- 将 “Write/SearchReplace” 改为 “Write”（并强调通过 `Read` 精准读取 + `Write` 覆盖写回来实现局部修改）
- 如果出现 `LS`/Shell 等表述，改为明确禁止

执行校验（见 Task 2）以确保文件中不再出现 `SearchReplace` 等字符串。

## Task 2: Add regression checks (local) for the prompt

**Files:**
- Modify: `src/system-prompt.md`

- [ ] **Step 1: Add/confirm minimal examples align with contract**

检查 Prompt 中已有示例是否会诱导输出冗长内容；如示例为“极简”，保留；如示例包含大量上下文，改为符合 Contract 的模板（只包含必要字段）。

- [ ] **Step 2: Run string-based contract checks**

Run (from repo root):

```bash
python -m json.tool src/memory-schema.json > /dev/null
python scripts/validate_reviews.py
git --no-pager grep -n "SearchReplace\\|actions/checkout@\\|\\bLS\\b" -- src/system-prompt.md
```

Expected:
- 前两条命令退出码为 0
- `git grep` 对 `SearchReplace` 与 `LS` 不应命中（`actions/checkout@` 可能存在于 workflow，不应出现在 system prompt）

- [ ] **Step 3: Optional CI sanity check (no commit required)**

Run:

```bash
python scripts/validate_reviews.py
```

Expected: `validated 2 review file(s)`（或更大数量）

## Task 3: Update docs (optional follow-up)

**Files:**
- Optional modify: `review_memory_skill_spec.md`

- [ ] **Step 1: Add a short note about schema flattening**

在该文档中补一段勘误：仓库当前 `src/memory-schema.json` 已扁平化，不再使用 `system_meta/metadata/...` 的示例结构；并指向最新 schema 文件。

- [ ] **Step 2: Verify doc references remain accurate**

Run:

```bash
git --no-pager grep -n "system_meta\\|metadata\\|key_findings\\|lessons_learned" -- src/memory-schema.json
```

Expected: 无命中（证明 schema 已扁平化，文档修订应与之对齐）

---

## Plan Self-Review

- Spec coverage:
  - 工具白名单：Task 1 Step 3 覆盖
  - 存储契约：Task 1 Step 2 覆盖
  - 写入/查询模板与禁止项：Task 1 Step 2 覆盖
  - 读取硬阈值：Task 1 Step 2 覆盖
- Placeholder scan:
  - 本计划未包含 TBD/TODO；每一步提供了明确的插入内容与命令
- Type consistency:
  - required 字段名与 `src/memory-schema.json` 保持一致（顶层字段）

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-17-prompt-contract-implementation-plan.md`.

Two execution options:
1. Subagent-Driven (recommended) — 我为每个 Task 派发一个独立子代理执行与自检，我逐步复核
2. Inline Execution — 在当前会话按 Task/Step 顺序直接实现并本地验证

你选择哪一种？
