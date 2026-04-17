# .gitignore 修正与 CI 缓存策略调整设计文档

## 背景
1. 当前仓库的 `.gitignore` 文件末尾存在格式错误（包含字面量的转义字符 `\n__pycache__/\n.pytest_cache/`），导致 Python 的编译缓存文件（如 `*.pyc`）和 pytest 缓存目录未能被正确忽略，从而被错误地提交到了版本库中。
2. 之前的 `memory_ci.yml` 包含了一个试图将生成的 `.cache/reviews/search_index.json` 自动提交回仓库的步骤。经过确认，我们决定采取“检索缓存不进入版本库，仅在本地/CI中按需生成”的策略。

## 目标
1. 修复 `.gitignore` 规则，确保后续 Python 和测试缓存不再被追踪。
2. 从 Git 历史（或至少从当前索引）中清除已经被错误提交的编译缓存文件。
3. 调整 `memory_ci.yml`，移除其自动提交 `search_index.json` 的步骤，仅保留“成功构建检索索引”以验证脚本正常运行。

## 方案范围 (In Scope)
### 1. 修改 `.gitignore`
- 移除损坏的最后一行。
- 新增标准规则：
  ```
  # Python
  __pycache__/
  *.py[cod]
  *$py.class
  
  # Pytest
  .pytest_cache/
  ```

### 2. 清理已被追踪的文件
使用 `git rm --cached` 移除仓库中现存的 `__pycache__` 目录及其下的 `.pyc` 文件。本地文件将保留。

### 3. 修改 `.github/workflows/memory_ci.yml`
- 删除 `build-cache` Job 中的 `Commit and push changes` 步骤及其相关权限配置。
- 保留 `Build search index` 步骤，以此作为一次冒烟测试，证明缓存构建脚本在当前代码和数据下能正常执行而不报错。

## 验收标准
1. `git status` 不会显示工作区内的 `.pyc` 文件或 `__pycache__` 目录。
2. `git diff --cached` 能够看到 `*.pyc` 文件被标为 deleted（从版本库移除）。
3. `memory_ci.yml` 的 `build-cache` 阶段将不再包含任何 Git 提交相关的命令。