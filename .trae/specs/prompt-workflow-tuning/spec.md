# 纯 Prompt 与工作流调优 Spec

## Why
当前阶段，我们希望通过最简单的原生能力（`Read`、`Write`、`Glob`、`Grep`）来验证并固化 `dao-genesis` 记忆管理技能的运转机制。在引入复杂的 MCP Server 前，充分打磨大模型的 System Prompt 和工作流（Workflow），以确保基础的上下文理解、结构化信息提取和 Token 控制机制能够稳定、低成本地运行。

## What Changes
- **优化 System Prompt**：在 `src/system-prompt.md` 中强化对工具调用的明确约束（如仅允许使用 `Read/Write/Glob/Grep`），并细化结构化输出（极简返回）的要求。
- **验证 JSON Schema 契约**：确保 `src/memory-schema.json` 中的必填字段和数据类型能够被当前 Prompt 完美适配。
- **构建测试工作流用例**：在 `.storage/reviews/` 中建立一条或多条 Mock 记忆数据，用于后续检索和更新链路的验证。

## Impact
- Affected specs: 基础复盘与记忆存取能力。
- Affected code: `src/system-prompt.md`、`src/memory-schema.json`、新增 Mock 数据（如 `.storage/reviews/REV-20260417-001.json`）。

## ADDED Requirements
### Requirement: 严格的工具约束与输出格式
大模型在执行记忆查询、写入和更新时：
- **WHEN** 触发“复盘”或“查询记忆”指令时
- **THEN** 必须严格遵循“只返回极简核心结论”或“仅返回 `review_id`”，严禁大段输出完整的 JSON 内容。

## MODIFIED Requirements
### Requirement: Prompt 工作流优化
细化 `src/system-prompt.md` 中关于多文件操作时的具体行为（如先 `Glob` 查找，再 `Read`，最后 `Write`），减少模型的探索成本。