# 全局记忆跨项目 Git 同步机制设计说明

## 1. 背景与目标
目前 `dao-genesis` 在项目级别实现了很好的记忆管理，但个人/团队往往希望经验能在多个项目间流转。根据 `spec.md` 中的设计，我们将引入一个专门的全局目录（默认为 `~/.trae/global_storage/reviews/`），用于存放脱离具体项目上下文的全局经验。
为了解决跨设备的同步问题，我们将开发一个基于专用 Git 仓库的同步脚本（类似 Obsidian Git），实现一键初始化、拉取和推送全局记忆。

## 2. 核心功能设计
新增脚本 `scripts/sync_global.py`，支持以下子命令：

### 2.1 `init <git_repo_url>`
- 检查 `MEMORY_GLOBAL_ROOT`（即 `~/.trae/global_storage/`）是否存在。
- 如果不存在，则克隆指定的 Git 仓库到该目录。
- 如果存在且为空，则初始化 Git 仓库并添加 Remote。
- 如果存在且已有 Git 仓库，则报错或提示已初始化。

### 2.2 `push`
- 在 `MEMORY_GLOBAL_ROOT` 执行 `git add .`。
- 如果没有更改，则提示无需同步。
- 否则，执行 `git commit -m "chore(memory): auto-sync global memory"`，并 `git push` 到远程。
- 此命令可以将本地提取的通用经验推送到全局仓库。

### 2.3 `pull`
- 在 `MEMORY_GLOBAL_ROOT` 执行 `git pull --rebase`。
- 如果遇到冲突，抛出明确错误并建议用户手动解决。
- 此命令用于在新设备或新项目中，同步别人或自己以前提交的全局经验。

### 2.4 `share <review_id>` (可选高级功能)
- 将当前项目的某个复盘文件从 `.storage/reviews/` 复制/软链接到 `MEMORY_GLOBAL_ROOT/reviews/` 中，以方便将其贡献为全局记忆。

## 3. 技术实现细节
- 依赖：Python `subprocess` 模块调用系统原生的 `git` 命令，这要求用户的系统环境已经配置好 Git 及其鉴权（SSH/HTTPS）。
- 环境变量：脚本默认从 `scripts/config.py` 获取 `MEMORY_GLOBAL_ROOT` 的路径。

## 4. 输出契约
- 尽量抑制原生 Git 命令的冗长输出（重定向 stdout/stderr），仅在报错时打印详情。
- 提供类似于 `[Sync] 成功拉取最新全局记忆` 或 `[Sync] 无需推送，已是最新` 的极简终端反馈。

## 5. 验收标准
1. `python scripts/sync_global.py init <repo>` 能成功拉取空仓库或带有复盘的仓库。
2. 往全局目录放一个文件后，执行 `push` 能成功提交并在终端看到成功提示。
3. 执行 `pull` 时能将远程最新文件拉下来。