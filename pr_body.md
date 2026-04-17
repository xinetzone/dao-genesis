此次合并引入了记忆注入工具（Memory Injector）和严格的 Prompt 契约，以规范系统复盘的写入与查询流程。它扁平化了记忆记录的结构，并新增了数据校验脚本与相关的单元测试。这些核心更改旨在优化多文件操作的 Token 消耗，提高自动化记录解析的容错性。

| 文件 | 变更 |
|------|---------|
| .github/workflows/ci.yml | - 为 CI 工作流添加了权限与并发控制设置<br>- 强制 JavaScript action 使用 Node.js 24 运行环境<br>- 新增了运行 `validate_reviews.py` 脚本验证复盘记录的步骤 |
| .gitignore | - 修改了忽略规则以保留 `.storage/reviews/*.json` 文件<br>- 添加了 Python 缓存目录 `.pycache/` 和 `.pytest_cache/` |
| .storage/reviews/REV-20260417-001.json | - 新增了关于功能实现的 JSON 格式复盘记录模拟数据 |
| .storage/reviews/REV-20260417-002.json | - 新增了关于系统复盘和记忆技能创建的 JSON 格式复盘记录模拟数据 |
| .storage/reviews/REV-20260417-003.json | - 新增了关于开发 CLI 辅助工具的 JSON 格式复盘记录模拟数据 |
| README.md | - 补充了记忆注入工具的命令行使用说明<br>- 增加了遵循 Contract 的查询演示小节和读取硬阈值说明<br>- 更新了更新与归档记忆的示例指令 |
| docs/superpowers/plans/2026-04-17-prompt-contract-implementation-plan.md | - 新增了在 System Prompt 中落地 Prompt 契约的实施计划文档 |
| docs/superpowers/plans/2026-04-17-readme-query-demo-plan.md | - 新增了在 README 中补充查询演示小节的实施计划文档 |
| docs/superpowers/specs/2026-04-17-inject-memory-normalization-design.md | - 新增了关于增强 Markdown 数组字段自动归一化解析能力的设计文档 |
| docs/superpowers/specs/2026-04-17-prompt-contract-design.md | - 新增了关于优化 Prompt 落地与契约分区的设计文档 |
| docs/superpowers/specs/2026-04-17-readme-query-demo-design.md | - 新增了 README 中查询演示小节的设计文档 |
| review_memory_skill_spec.md | - 将文档版本更新为 1.1.0 并补充了 Contract 强约束说明<br>- 将 JSON 结构示例更新为扁平化格式<br>- 强调了极致精简输出与多文件操作顺序的 Token 优化要求 |
| scripts/__pycache__/inject_memory.cpython-314.pyc | - 新增了 `inject_memory.py` 的编译缓存文件 |
| scripts/inject_memory.py | - 创建了将 Markdown 复盘笔记解析并转换为合规 JSON 记录的 Python 脚本 |
| scripts/run_tests.sh | - 新增了用于在本地或 CI 环境中执行单元测试与数据校验的 Shell 脚本 |
| scripts/validate_reviews.py | - 创建了用于验证 JSON 复盘记录是否符合 Schema 定义的 Python 校验脚本 |
| src/system-prompt.md | - 新增了 Contract 区块以严格限制工具白名单、存储契约与极简输出要求<br>- 更新了多文件操作指南，明确禁止使用 Shell 命令操作文件内容<br>- 修改了查询和代码审查示例，以演示极致的 Token 优化返回格式 |
| tests/__init__.py | - 新增了空的包初始化文件 |
| tests/__pycache__/__init__.cpython-314.pyc | - 新增了 `__init__.py` 的编译缓存文件 |
| tests/__pycache__/test_inject_memory.cpython-314-pytest-9.0.2.pyc | - 新增了测试脚本的编译缓存文件 |
| tests/test_inject_memory.py | - 新增了针对 `inject_memory.py` 解析和转换逻辑的单元测试脚本 |