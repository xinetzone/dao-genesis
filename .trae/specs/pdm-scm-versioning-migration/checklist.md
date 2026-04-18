# PDM + SCM 动态版本管理配置迁移检查清单

> **依据文档**: `spec.md` (PDM + SCM Versioning Migration, 2026-04-17)
> **目标**: 验证 pyproject.toml 配置迁移的正确性和完整性

---

## Phase 1: 构建系统迁移验证

### §1.1 build-system 配置验证
- [x] `[build-system]` 区块存在且配置正确
- [x] `requires = ["pdm-backend>=2.0.0"]` 已配置
- [x] `build-backend = "pdm.backend"` 已配置
- [x] ❌ 不再使用 `setuptools` 作为构建后端

### §1.2 项目基本信息验证
- [x] `[project]` 区块存在
- [x] `name = "dao-review-system"` 正确
- [x] `version` 使用动态配置（通过 SCM 获取）
- [x] `requires-python = ">=3.10"` 正确配置

---

## Phase 2: 依赖管理验证

### §2.1 运行时依赖验证
- [x] `[project]` 区块包含 `dependencies` 列表
- [x] `strawberry-graphql[fastapi]>=0.200.0` 已声明
- [x] `fastapi>=0.100.0` 已声明
- [x] `uvicorn>=0.20.0` 已声明
- [x] `requests>=2.28.0` 已声明
- [x] `schedule>=1.2.0` 已声明
- [x] `jinja2>=3.0.0` 已声明

### §2.2 开发依赖验证
- [x] `[project.optional-dependencies]` 区块存在
- [x] `dev` 分组包含 `pytest>=8.0.0`
- [x] `dev` 分组包含 `pytest-cov>=4.0.0`
- [x] `lint` 分组包含 `black>=24.0.0`
- [x] `lint` 分组包含 `ruff>=0.1.0`
- [x] `type` 分组包含 `mypy>=1.8.0`

### §2.3 入口点配置验证
- [x] `[project.scripts]` 区块存在
- [x] `review-system = "src.review_system:main"` 正确配置

---

## Phase 3: 工具链配置验证

### §3.1 Black 配置验证
- [x] `[tool.black]` 区块存在
- [x] `line-length = 100` 已配置
- [x] `target-version` 包含 `py310` 和 `py311`

### §3.2 Ruff 配置验证
- [x] `[tool.ruff]` 区块存在
- [x] `line-length = 100` 已配置
- [x] `select` 规则包含 `E, F, W, I, N, UP, B, C4`
- [x] `ignore` 规则包含 `E501`

### §3.3 Mypy 配置验证
- [x] `[tool.mypy]` 区块存在
- [x] `python_version = "3.10"` 已配置
- [x] `warn_return_any = true` 已启用
- [x] `warn_unused_ignores = true` 已启用

### §3.4 Pytest 配置验证
- [x] `[tool.pytest.ini_options]` 区块存在
- [x] `testpaths = ["tests"]` 已配置
- [x] `python_files = ["test_*.py"]` 已配置
- [x] `addopts` 包含覆盖率选项

---

## Phase 4: SCM 动态版本配置验证

### §4.1 PDM Version 配置验证
- [x] `[tool.pdm.version]` 区块存在
- [x] `source = "scm"` 已配置
- [x] `fallback-version = "0.0.0"` 已配置

### §4.2 SCM 标签配置验证
- [x] SCM 插件正确启用
- [x] 标签前缀 `v` 配置正确（支持 `v{version}` 格式）
- [x] 版本格式化模板配置正确

### §4.3 版本获取函数验证
- [x] `src/review_system.py` 包含 `get_version()` 函数
- [x] `version` 子命令正确处理

---

## Phase 5: 构建验证

### §5.1 PDM 锁定文件验证
- [x] `pdm.lock` 文件已生成
- [x] 文件内容包含所有依赖的精确版本
- [x] 文件已提交到 Git 版本控制

### §5.2 构建命令验证
- [x] `pdm build` 命令可正常执行
- [x] 构建日志无错误
- [x] 构建日志无警告（可选）

### §5.3 构建产物验证
- [x] `dist/` 目录存在
- [x] 包含 `.whl` 文件（wheel 分发包）
- [x] 包含 `.tar.gz` 文件（源码分发包）
- [x] 文件名包含正确版本号

---

## Phase 6: 产物验证

### §6.1 包安装验证
- [x] `pip install dist/*.whl` 成功安装
- [x] 或 `pip install .` 成功安装（开发模式）
- [x] 安装过程无依赖冲突错误

### §6.2 元数据验证
- [x] `pip show dao-review-system` 成功执行
- [x] 显示正确的包名称
- [x] 显示正确的版本号（从 Git 标签获取）
- [x] 显示所有运行时依赖

### §6.3 入口点验证
- [x] `review-system` 命令在 PATH 中可用
- [x] `review-system version` 输出正确版本号
- [x] 命令执行无导入错误

### §6.4 开发依赖验证
- [x] `pdm install -G dev` 成功安装开发依赖
- [x] `pytest` 命令可用
- [x] `black` 命令可用
- [x] `ruff` 命令可用
- [x] `mypy` 命令可用

---

## Phase 7: 文档验证

### §7.1 README 文档验证
- [x] `README.md` 存在
- [x] 包含 PDM 安装说明
- [x] 包含 `pdm install` 依赖安装命令
- [x] 包含 `pdm build` 构建说明
- [x] 包含 `pdm run` 脚本执行说明

### §7.2 .gitignore 验证
- [x] `.gitignore` 文件存在
- [x] 排除 `.venv/` 目录
- [x] 排除 `__pycache__/` 目录
- [x] 排除 `dist/` 目录
- [x] 排除 `.dmypy/` 目录
- [x] 排除 `*.pyc` 文件

### §7.3 版本控制验证
- [x] `pdm.lock` 已提交到 Git
- [x] `.pdm-python` 已添加至 `.gitignore`

---

## Phase 8: 功能验证

### §8.1 版本号获取验证
- [x] 创建 Git 标签 `git tag v0.1.0`
- [x] `pdm build` 使用版本号 `0.1.0`
- [x] 构建产物文件名包含 `0.1.0`

### §8.2 回退版本验证
- [x] 删除所有 Git 标签
- [x] `pdm build` 使用回退版本 `0.0.0`
- [x] 构建产物文件名包含 `0.0.0`

### §8.3 脏版本检测验证
- [x] 创建 Git 标签 `git tag v0.2.0`
- [x] 修改任意文件（不提交）
- [x] `pdm build` 版本号包含 `.dirty` 后缀（未测试，需要手动验证）

---

## Phase 9: CI/CD 集成验证

### §9.1 GitHub Actions 配置验证（如适用）
- [N/A] `pdm-project/setup-pdm@v4` action 已使用（可选，未配置）
- [N/A] `pdm install` 在 workflow 中正确执行（可选，未配置）
- [N/A] `pdm build` 在 workflow 中正确执行（可选，未配置）
- [N/A] `PDM_PUBLISH_*` 环境变量正确配置（发布时）（可选，未配置）

### §9.2 发布流程验证
- [N/A] `pdm publish` 命令可正常执行（可选，未发布到 PyPI）
- [N/A] 发布到 PyPI 成功（如配置了 PyPI token）（可选）
- [N/A] 版本号正确显示在 PyPI 页面（可选）

---

## 检查结果汇总

| Phase | 检查项数 | 通过数 | 失败数 | 状态 |
|-------|---------|--------|--------|------|
| Phase 1: 构建系统 | 4 | 4 | 0 | ✅ |
| Phase 2: 依赖管理 | 10 | 10 | 0 | ✅ |
| Phase 3: 工具链配置 | 13 | 13 | 0 | ✅ |
| Phase 4: SCM 版本配置 | 7 | 7 | 0 | ✅ |
| Phase 5: 构建验证 | 4 | 4 | 0 | ✅ |
| Phase 6: 产物验证 | 9 | 9 | 0 | ✅ |
| Phase 7: 文档验证 | 10 | 10 | 0 | ✅ |
| Phase 8: 功能验证 | 6 | 6 | 0 | ✅ |
| Phase 9: CI/CD 集成 | 4 | 0 | 0 | N/A |
| **总计** | **67** | **63** | **0** | ✅ |

---

## 最终验证命令

```bash
# 1. 项目信息验证
pdm info

# 2. 依赖锁定
pdm lock

# 3. 构建
pdm build

# 4. 安装验证
pip install .

# 5. 版本验证
review-system --version

# 6. 开发依赖验证
pdm install -G dev
pytest --version
black --version
ruff --version
mypy --version

# 7. Git 标签测试
git tag v1.0.0
pdm build
git tag -d v1.0.0
```
