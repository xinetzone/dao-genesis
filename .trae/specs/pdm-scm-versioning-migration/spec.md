# PDM + SCM 动态版本管理配置迁移规范

## Why

当前项目 `d:\xinet\daoCollective\Dao\dao-genesis\pyproject.toml` 使用传统的 `setuptools` 构建系统，版本号 `0.1.0` 为静态值，无法与 Git 提交历史和标签保持同步。这导致手动维护版本号容易出错，且无法实现自动化发布流程。需要迁移到 PDM 包管理器，并集成 SCM 功能实现版本号的自动化管理。

## What Changes

- 将 `[build-system]` 从 `setuptools` 迁移到 `pdm-backend`
- 将依赖管理方式从 pip/setuptools 迁移到 PDM
- 配置动态版本号管理，版本号根据 Git 标签自动获取
- 集成 Git SCM 功能，版本信息与提交历史同步
- 添加 PEP 621 标准依赖配置格式
- 配置开发依赖组和工具链

## Impact

- Affected specs：
  - 项目配置管理（pyproject.toml）
  - 依赖管理规范
  - 版本管理规范
  - 构建发布流程

- Affected code：
  - `pyproject.toml` - 项目根配置文件
  - 无需修改业务代码

## ADDED Requirements

### Requirement: PDM 项目结构配置

项目必须采用 PDM 作为包管理器，遵循 PEP 621 规范。

#### Scenario: PDM 项目初始化
- **WHEN** 使用 PDM 管理项目依赖时
- **THEN** 必须使用 `pdm-backend` 作为构建后端
- **AND** `pyproject.toml` 必须包含 `[project]` 和 `[tool.pdm]` 区块

```toml
[build-system]
requires = ["pdm-backend>=2.0.0"]
build-backend = "pdm.backend"

[project]
name = "dao-review-system"
version = "0.1.0"
requires-python = ">=3.10"
```

### Requirement: 动态版本号管理

项目版本号必须通过 SCM（源代码管理）自动获取，实现版本号与 Git 标签同步。

#### Scenario: 从 Git 标签获取版本号
- **WHEN** 构建项目或查询版本信息时
- **THEN** 系统 SHALL 从 Git 标签（如 `v0.1.0`）自动提取版本号
- **AND** 版本号格式遵循语义化版本（SemVer）规范：`MAJOR.MINOR.PATCH`

#### 版本号获取规则

| Git 标签格式 | 提取版本号 | 示例 |
|-------------|-----------|------|
| `v{version}` | 去除 `v` 前缀 | `v1.2.3` → `1.2.3` |
| `{version}` | 直接使用 | `1.2.3` → `1.2.3` |
| 无标签 | 回退到 `0.0.0` + commit hash | `0.0.0+d20260417` |

#### 动态版本号配置

```toml
[tool.pdm.version]
source = "scm"
fallback-version = "0.0.0"

[tool.pdm.scripts]
version = {call = "src.review_system:get_version"}
```

### Requirement: SCM 集成功能

系统 SHALL 集成 Git SCM 功能，确保版本信息与源代码管理保持同步。

#### SCM 集成能力

| SCM 功能 | 说明 | 实现方式 |
|---------|------|---------|
| **标签读取** | 从 Git 标签提取版本号 | PDM 内置 SCM 插件 |
| **提交历史** | 获取当前 commit 的 hash 和时间 | Git CLI 或 PDM |
| **脏版本检测** | 检测未提交的更改 | SCM `dirty` 标志 |
| **版本格式化** | 组合版本号 + 提交信息 | `f"{version}+d{date}.{hash}"` |

#### 版本字符串格式

| 场景 | 版本字符串格式 | 示例 |
|-----|--------------|------|
| 正式发布 | `{version}` | `1.2.3` |
| 开发版本 | `{version}+d{date}.{hash}` | `1.2.3+d20260417.abc1234` |
| 脏版本 | `{version}+d{date}.{hash}.dirty` | `1.2.3+d20260417.abc1234.dirty` |

### Requirement: 依赖管理配置

项目依赖必须采用 PEP 621 标准格式，通过 PDM 管理。

#### 依赖分组配置

```toml
[project]
dependencies = [
    "strawberry-graphql[fastapi]>=0.200.0",
    "fastapi>=0.100.0",
    "uvicorn>=0.20.0",
    "requests>=2.28.0",
    "schedule>=1.2.0",
    "jinja2>=3.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "black>=24.0.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
]
```

#### 开发依赖安装命令

```bash
pdm install -G dev
```

### Requirement: 工具链配置

项目必须配置代码质量工具链（格式化、类型检查、测试）。

#### 工具配置清单

| 工具 | 配置区块 | 功能 |
|------|---------|------|
| **Black** | `[tool.black]` | 代码格式化 |
| **Ruff** | `[tool.ruff]` | Linting（替代 flake8） |
| **Mypy** | `[tool.mypy]` | 静态类型检查 |
| **Pytest** | `[tool.pytest.ini_options]` | 测试框架 |
| **PDLint** | `[tool.pdm-lint]` | PDM 配置检查 |

#### 工具配置示例

```toml
[tool.black]
line-length = 100
target-version = ["py310", "py311"]

[tool.ruff]
line-length = 100
select = ["E", "F", "W", "I", "N", "UP", "B", "C4"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --cov=src --cov-report=term-missing"
```

### Requirement: 构建产物验证

构建完成后必须验证产物正确性，确保动态版本号已正确嵌入。

#### 产物验证清单

| 验证项 | 验证方式 | 预期结果 |
|-------|---------|---------|
| **包文件存在** | `ls dist/` | 包含 `.whl` 或 `.tar.gz` |
| **版本号嵌入** | `pip show dao-review-system` | 显示正确版本号 |
| **元数据正确** | `pdm build` 输出 | 无错误信息 |
| **依赖完整** | `pip install -e .` | 所有依赖正确安装 |

## MODIFIED Requirements

### Requirement: 项目入口点配置

原有的 `[scripts]` 配置需要迁移到 PDM 格式。

#### 原有配置（setuptools）
```toml
[scripts]
review-system = "src.review_system:main"
```

#### 新配置（PDM）
```toml
[project.scripts]
review-system = "src.review_system:main"
```

## REMOVED Requirements

### Requirement: setuptools 构建系统

**Reason**: PDM 要求使用 `pdm-backend` 作为构建后端以支持动态版本号功能

**Migration**:
1. 将 `requires = ["setuptools>=42", "wheel"]` 改为 `requires = ["pdm-backend>=2.0.0"]`
2. 将 `build-backend = "setuptools.build_meta"` 改为 `build-backend = "pdm.backend"`

## Technical Implementation Details

### PDM SCM 版本插件配置

```toml
[tool.pdm.version]
source = "scm"

[tool.pdm.scm.sources]
format = "short"
dirty = true
template = "{version}+d{date}"

[tool.pdm.scm.rev]
append_to = "tag"
prefix = "v"
```

### 版本获取优先级

1. **Git 标签** - 优先从 `v{version}` 标签提取
2. **环境变量** - `PDM_VERSION_OVERRIDE` 可覆盖自动检测
3. **回退版本** - `fallback-version = "0.0.0"` 指定默认值

### CI/CD 集成

```yaml
# GitHub Actions 示例
- name: Build and publish
  run: |
    pdm install
    pdm build
  env:
    PDM_PUBLISH_REPO: pypi
```

## 验证流程

1. 执行 `pdm install` 验证依赖安装
2. 执行 `pdm build` 验证构建过程
3. 检查 `dist/` 目录中的产物版本号
4. 执行 `pip show dao-review-system` 验证元数据
5. 执行 `pdm run review-system --version` 验证运行时版本
