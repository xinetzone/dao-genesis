# PDM + SCM 动态版本管理配置迁移任务清单

> **基于**: `spec.md` (PDM + SCM Versioning Migration, 2026-04-17)
> **目标**: 将项目从 setuptools 迁移到 PDM，实现动态版本号管理和 SCM 集成

---

## 任务依赖关系

```
Task 1 (pyproject.toml 配置) ──────────────────────────────────────────┐
     │                                                                  │
     ├──→ Task 2 (依赖迁移) ──→ Task 3 (工具链配置)                     │
     │                                                    │             │
     │                                                    ▼             │
     └──→ Task 4 (版本管理配置) ←───────────────────────────────────────┤
                │                                                       │
                ▼                                                       │
           Task 5 (构建验证) ──→ Task 6 (产物验证) ──→ Task 7 (文档更新)
```

---

## Task 1: 修改 pyproject.toml 构建系统配置

### 目标
将 `[build-system]` 从 setuptools 迁移到 pdm-backend，启用 PDM 包管理

### 任务步骤
- [x] 1.1 修改 `[build-system]` 区块：
  - [x] 将 `requires = ["setuptools>=42", "wheel"]` 改为 `requires = ["pdm-backend>=2.0.0"]`
  - [x] 将 `build-backend = "setuptools.build_meta"` 改为 `build-backend = "pdm.backend"`
- [x] 1.2 添加 `[tool.pdm]` 基础配置区块
- [x] 1.3 保留 `[project]` 区块的基本信息（name, version, description）
- [x] 1.4 迁移 `[scripts]` 到 `[project.scripts]`（PEP 621 标准格式）

### 验证标准
- `pdm init` 可正确识别项目配置
- `pdm info` 显示正确的项目信息

---

## Task 2: 依赖管理迁移

### 目标
将依赖配置迁移到 PEP 621 标准格式，通过 PDM 管理

### 任务步骤
- [ ] 2.1 迁移 `[project.dependencies]` 依赖列表：
  - [ ] 保留 `strawberry-graphql[fastapi]>=0.200.0`
  - [ ] 保留 `fastapi>=0.100.0`
  - [ ] 保留 `uvicorn>=0.20.0`
  - [ ] 保留 `requests>=2.28.0`
  - [ ] 保留 `schedule>=1.2.0`
  - [ ] 保留 `jinja2>=3.0.0`
- [ ] 2.2 添加 `[project.optional-dependencies]` 开发依赖组：
  - [ ] 添加 `dev` 分组：`pytest>=8.0.0`, `pytest-cov>=4.0.0`
  - [ ] 添加 `lint` 分组：`black>=24.0.0`, `ruff>=0.1.0`
  - [ ] 添加 `type` 分组：`mypy>=1.8.0`
- [ ] 2.3 更新 `requires-python` 为 `">=3.10"`（PDM 兼容 Python 3.10+）
- [ ] 2.4 移除旧的 `classifiers` 字段（PDM 自动生成）
- [ ] 2.5 移除旧的 `authors` 字段或迁移到标准格式

### 验证标准
- `pdm add <package>` 可正常添加依赖
- `pdm lock` 可成功生成 `pdm.lock` 文件
- `pdm install -G dev` 可正确安装开发依赖

---

## Task 3: 工具链配置

### 目标
配置代码质量工具（Black, Ruff, Mypy, Pytest）

### 任务步骤
- [ ] 3.1 配置 `[tool.black]` 代码格式化：
  - [ ] 设置 `line-length = 100`
  - [ ] 设置 `target-version = ["py310", "py311"]`
- [ ] 3.2 配置 `[tool.ruff]` Linting（替代 flake8）：
  - [ ] 设置 `line-length = 100`
  - [ ] 配置 `select` 规则：`E, F, W, I, N, UP, B, C4`
  - [ ] 配置 `ignore` 规则：`E501`
- [ ] 3.3 配置 `[tool.mypy]` 静态类型检查：
  - [ ] 设置 `python_version = "3.10"`
  - [ ] 启用 `warn_return_any = true`
  - [ ] 启用 `warn_unused_ignores = true`
- [ ] 3.4 配置 `[tool.pytest.ini_options]` 测试框架：
  - [ ] 设置 `testpaths = ["tests"]`
  - [ ] 设置 `python_files = ["test_*.py"]`
  - [ ] 添加 `addopts = "-v --cov=src --cov-report=term-missing"`
- [ ] 3.5 配置 `[tool.pdm-lint]` PDM 配置检查

### 验证标准
- `pdm run black .` 可格式化代码
- `pdm run ruff check .` 可检查代码
- `pdm run mypy src` 可进行类型检查
- `pdm run pytest` 可运行测试

---

## Task 4: SCM 动态版本号配置

### 目标
配置 PDM 内置 SCM 插件，实现版本号自动从 Git 标签获取

### 任务步骤
- [ ] 4.1 添加 `[tool.pdm.version]` 配置：
  - [ ] 设置 `source = "scm"`
  - [ ] 设置 `fallback-version = "0.0.0"`
- [ ] 4.2 配置 SCM 标签格式：
  - [ ] 设置 `tag_prefix = "v"`（支持 `v1.2.3` 格式标签）
  - [ ] 设置版本格式化模板
- [ ] 4.3 配置版本脚本 `get_version()` 函数：
  - [ ] 在 `src/review_system.py` 中实现版本获取函数
  - [ ] 支持 `--version` 参数输出版本信息
- [ ] 4.4 测试版本号获取：
  - [ ] 创建 Git 标签 `git tag v0.1.0`
  - [ ] 验证 `pdm build` 使用正确版本号
  - [ ] 验证无标签时的回退版本 `0.0.0`

### 验证标准
- `git tag v0.1.0 && pdm build` 构建产物版本为 `0.1.0`
- 无 Git 标签时版本回退到 `0.0.0`
- 脏版本（未提交更改）标记 `.dirty` 后缀

---

## Task 5: 构建验证

### 目标
验证 PDM 可正常构建项目并生成产物

### 任务步骤
- [x] 5.1 执行 `pdm lock` 生成锁定文件
- [x] 5.2 执行 `pdm build` 构建分发包
- [x] 5.3 检查 `dist/` 目录内容
- [x] 5.4 验证 `.whl` 和 `.tar.gz` 文件生成
- [x] 5.5 验证构建日志无错误和警告

### 验证标准
- `dist/` 包含正确版本号的包文件
- 构建日志无 `Resolution Impossible` 错误
- 产物可被 `pip install` 正确安装

---

## Task 6: 产物验证

### 目标
验证构建产物的正确性和完整性

### 任务步骤
- [x] 6.1 安装构建产物：
  - [x] 使用 `pip install dist/*.whl` 安装
  - [x] 或使用 `pip install .` 安装源码
- [x] 6.2 验证包元数据：
  - [x] 执行 `pip show dao-review-system`
  - [x] 确认版本号正确
  - [x] 确认依赖列表完整
- [x] 6.3 验证入口点：
  - [x] 执行 `review-system version` 验证命令可用
  - [x] 验证输出包含正确版本号
- [x] 6.4 验证开发依赖：
  - [x] 执行 `pdm install -G dev`
  - [x] 验证 pytest、black 等工具可用

### 验证标准
- `pip show` 显示正确的版本号和依赖
- `review-system` 命令可正常执行
- `pdm install -G dev` 成功安装所有开发依赖

---

## Task 7: 文档更新

### 目标
更新项目文档以反映 PDM 迁移的变更

### 任务步骤
- [ ] 7.1 更新或创建 `README.md`：
  - [ ] 添加 PDM 安装说明
  - [ ] 添加 `pdm install` 依赖安装命令
  - [ ] 添加 `pdm build` 构建说明
  - [ ] 添加 `pdm run` 脚本执行说明
- [ ] 7.2 创建或更新 `.gitignore`：
  - [ ] 排除 `.venv/` 虚拟环境目录
  - [ ] 排除 `__pycache__/` 缓存目录
  - [ ] 排除 `dist/` 构建产物目录
  - [ ] 排除 `.dmypy/` 类型检查缓存
- [ ] 7.3 创建 `CONTRIBUTING.md`（如需要）：
  - [ ] 添加开发环境设置步骤
  - [ ] 添加代码规范要求
  - [ ] 添加测试运行方法

### 验证标准
- README 包含完整的 PDM 使用说明
- .gitignore 正确排除临时文件和构建产物
- 团队成员可按照文档快速上手

---

## 任务完成标准

| 任务 | 完成标准 | 验证命令 |
|-----|---------|---------|
| Task 1 | pyproject.toml 使用 pdm-backend | `pdm info` |
| Task 2 | 依赖通过 PDM 管理，pdm.lock 生成 | `pdm lock` |
| Task 3 | 所有工具链配置正确 | `pdm run pytest` |
| Task 4 | 版本号从 Git 标签自动获取 | `git tag v0.1.0 && pdm build` |
| Task 5 | 构建成功，产物在 dist/ | `ls dist/` |
| Task 6 | 产物可安装，命令可执行 | `pip show dao-review-system` |
| Task 7 | 文档完整更新 | 人工审查 |

---

## 注意事项

1. **Python 版本要求**：PDM 要求 Python >= 3.10，请确保项目运行环境满足
2. **Git 仓库要求**：SCM 版本功能需要项目处于 Git 版本控制下
3. **标签命名规范**：版本标签必须使用 `v{version}` 格式（如 `v1.2.3`）
4. **锁定文件提交**：请将 `pdm.lock` 提交到版本控制，确保团队使用相同依赖版本
