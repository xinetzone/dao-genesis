# Tasks
- [x] Task 1: 优化系统提示词 (System Prompt)
  - [x] SubTask 1.1: 在 `src/system-prompt.md` 中增加明确的原生文件操作工具 (Read/Write/Glob/Grep) 使用指引。
  - [x] SubTask 1.2: 补充针对输出 Token 优化的“极简返回”强约束示例。
- [x] Task 2: 校验并对齐记忆数据结构 (Memory Schema)
  - [x] SubTask 2.1: 审查 `src/memory-schema.json`，确保字段定义与 Prompt 逻辑严格对应，无冗余嵌套。
- [x] Task 3: 构建 Mock 测试记忆库
  - [x] SubTask 3.1: 初始化 `.storage/reviews/` 目录。
  - [x] SubTask 3.2: 编写一个标准的 `REV-20260417-001.json` Mock 记忆文件，用于后续的检索和更新测试。

# Task Dependencies
- [Task 2] depends on [Task 1]
- [Task 3] depends on [Task 2]