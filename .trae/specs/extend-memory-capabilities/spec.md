# 扩展记忆管理能力 Spec

## Why
目前 `dao-genesis` 的系统性复盘与记忆管理技能需要人工通过自然语言或 CLI 工具手动触发。为了进一步提升效能并将其融入日常研发工作流中，需要对其进行三大方向的深度扩展：与 Issue Trackers 自动化闭环、基于工作区状态的上下文自动注入，以及记忆的生命周期管理与知识图谱构建。

## What Changes
- 增加 GitHub Actions 工作流与集成脚本，在 PR 合并时自动生成复盘记录并回写 Issue。
- 增加工作区上下文分析脚本，自动提取当前修改的文件和 Diff，主动召回相关历史记忆。
- 增加记忆生命周期管理脚本，支持基于时间或访问频率自动归档旧记忆。
- 增加知识图谱生成脚本，解析复盘 JSON 提取模块和问题的实体关系，生成可视化的关联图谱（如 Mermaid）。
- 在 `src/mcp_server.py` 中新增暴露上下文注入、生命周期管理和图谱生成的 MCP 工具。

## Impact
- Affected specs: 基础复盘与记忆存取能力。
- Affected code:
  - `.github/workflows/auto_review.yml` (新增)
  - `scripts/github_integration.py` (新增)
  - `scripts/context_injector.py` (新增)
  - `scripts/memory_lifecycle.py` (新增)
  - `scripts/knowledge_graph.py` (新增)
  - `src/mcp_server.py` (修改)

## ADDED Requirements
### Requirement: 与 Issue Trackers 深度集成
系统应当能够在代码合并时自动完成经验的沉淀与追踪闭环。
#### Scenario: 成功合并 PR 触发自动复盘
- **WHEN** 开发者在 GitHub 合并一个 Pull Request
- **THEN** CI 工作流被触发，自动拉取 PR 的 Diff 与评论，生成复盘 JSON 存入 `.storage/reviews`，并将复盘摘要以 Comment 的形式回写到该 PR 中。

### Requirement: 自动化上下文注入
系统应当能够基于当前工作状态，主动推荐相关的历史最佳实践和防错指南。
#### Scenario: 开始新任务或修改历史易错文件
- **WHEN** 开发者或 AI Agent 请求当前工作区上下文
- **THEN** 脚本分析当前未提交的 git diff 或活跃文件路径，自动检索并返回涉及这些文件的历史 `action_items` 与 `lessons_learned`。

### Requirement: 记忆生命周期与知识图谱
系统应当具备自我清理能力，并能从碎片化的记录中提取全局视角。
#### Scenario: 定期巡检与图谱构建
- **WHEN** 触发记忆生命周期巡检
- **THEN** 系统自动将超过设定阈值（如一年）且不属于基础架构的记录标记为 `archived`，同时生成反映模块间问题与决策关联的全局知识图谱。
