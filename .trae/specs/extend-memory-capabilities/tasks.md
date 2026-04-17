# Tasks

- [x] Task 1: 实现 Issue Trackers 自动化闭环 (GitHub Integration)
  - [x] SubTask 1.1: 创建 `.github/workflows/auto_review.yml` GitHub Actions 工作流，监听 Pull Request 的合并事件。
  - [x] SubTask 1.2: 开发 `scripts/github_integration.py` 脚本，获取 PR 的 Diff 和评论上下文，利用大模型生成符合 `memory-schema.json` 的复盘记录。
  - [x] SubTask 1.3: 实现将生成的复盘摘要和 `review_id` 以 Comment 的形式回写到原 PR 的逻辑。

- [x] Task 2: 实现自动化上下文注入 (Automated Context Injection)
  - [x] SubTask 2.1: 开发 `scripts/context_injector.py` 脚本，分析当前工作区的活跃文件（如未提交的 `git diff` 或近期被频繁修改的文件）。
  - [x] SubTask 2.2: 在该脚本中集成现有 `search_memory.py` 的查询逻辑，根据提取的文件路径和变更关键字自动召回相关历史记忆的 `action_items` 与结论。
  - [x] SubTask 2.3: 在 `src/mcp_server.py` 中新增一个 MCP 工具 `inject_context`，供 AI Agent 直接调用。

- [x] Task 3: 实现记忆生命周期与知识图谱 (Lifecycle & Knowledge Graph)
  - [x] SubTask 3.1: 开发 `scripts/memory_lifecycle.py` 脚本，实现基于创建时间和状态的定期清理逻辑（如将超过 1 年的非核心记录自动标记为 `archived`）。
  - [x] SubTask 3.2: 开发 `scripts/knowledge_graph.py` 脚本，解析 `.storage/reviews/` 下的所有活跃 JSON，提取 `tags`、`task_type` 和文件关联关系，生成 Mermaid 格式或标准 JSON 格式的知识图谱。
  - [x] SubTask 3.3: 在 `src/mcp_server.py` 中暴露 `archive_stale_memories` 和 `generate_knowledge_graph` 两个 MCP 工具。

- [x] Task 4: 补充测试与文档更新
  - [x] SubTask 4.1: 为新增的 `github_integration.py`、`context_injector.py`、`memory_lifecycle.py` 和 `knowledge_graph.py` 编写完整的 `pytest` 单元测试，确保覆盖率要求。
  - [x] SubTask 4.2: 更新 `README.md` 与 `review_memory_skill_spec.md`，记录新增自动化功能的使用方式和最佳实践。

# Task Dependencies
- [Task 4] depends on [Task 1], [Task 2], [Task 3]
