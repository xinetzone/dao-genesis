# README Query Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `README.md` 增加“查询演示（遵循 Contract）”小节，展示用户指令、内部工具流程（Glob→Grep→Read）、读取硬阈值与 Top N=3 的极简输出模板。

**Architecture:** 仅修改 README 文案，不新增脚本；演示内容严格复用 `src/system-prompt.md` 的 Contract（Top N=3、禁止输出完整 JSON、读取阈值等）。

**Tech Stack:** Markdown、git grep（本地一致性检查）。

---

## File Structure

- Modify: `README.md`
  - 在 `## 💬 使用示例 (Usage Examples)` 章节内新增 `### 查询演示（遵循 Contract）` 小节
- Reference (read-only):
  - `src/system-prompt.md`：Query Output Contract、Query Workflow (Token Limits)
  - `.storage/reviews/REV-*.json`：提供示例 review_id（如 `REV-20260417-002`）

---

### Task 1: Add query demo section to README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Locate insertion point**

Read: `README.md`  
目标：在 `## 💬 使用示例 (Usage Examples)` 段落里，紧跟现有“查询经验”示例后插入新小节，确保读者连续阅读。

- [ ] **Step 2: Insert the exact section content**

将以下内容插入 README（保持与现有引用风格一致）：

```text
### 查询演示（遵循 Contract）

用户指令示例：
> `@dao-genesis 查询记忆：schema 扁平化 工具白名单`

内部工具流程（用于调试与对齐 Contract）：
1) Glob：定位候选文件（`.storage/reviews/REV-*.json`）
2) Grep：用关键词初筛命中记录（必要时拆分多个关键词）
3) Read：仅读取少量命中文件片段以提炼“核心结论/行动项”

读取硬阈值：
- 最多读取 3 个文件
- 每个文件最多读取 120 行片段（必要时用 `offset/limit`）

期望输出（Top N=3，极简返回）：
- `REV-20260417-002` | 核心结论：Schema 扁平化降低写入难度 | 行动：统一工具白名单并补齐极简输出模板

禁止：
- 输出完整 JSON
- 输出整段原文/整份复盘报告
```

- [ ] **Step 3: Ensure formatting matches surrounding README**

检查：
- 是否需要将 `text` 块改为 Markdown（例如用普通段落 + 列表，而非 ```text```），以与 README 其他示例一致
- 引号与反引号是否统一（命令示例使用内联代码）

---

### Task 2: Local validation checks

**Files:**
- Modify: `README.md`
- Reference: `src/system-prompt.md`

- [ ] **Step 1: Verify README does not contradict Contract**

Run:

```bash
git --no-pager grep -n "Top N=3\\|最多读取 3 个文件\\|每个文件最多读取 120 行" -- README.md
```

Expected: 能找到新增小节中的关键约束文本。

- [ ] **Step 2: Sanity-check system prompt contract remains present**

Run:

```bash
git --no-pager grep -n "# Contract (Strict)" -- src/system-prompt.md
```

Expected: 命中 1 次（或更多，但至少 1 次）。

- [ ] **Step 3: Keep existing CI validations passing**

Run:

```bash
python scripts/validate_reviews.py
```

Expected: `validated N review file(s)`

---

## Plan Self-Review

- Spec coverage:
  - 用户指令、工具流程、硬阈值、输出模板、禁止项均在 Task 1 Step 2 覆盖
- Placeholder scan:
  - 无 TBD/TODO；插入内容为可直接粘贴的完整段落
- Consistency:
  - Top N=3 与读取阈值与 `src/system-prompt.md` 的 Contract 保持一致

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-17-readme-query-demo-plan.md`.

Two execution options:
1. Subagent-Driven (recommended)
2. Inline Execution

你选择哪一种？
