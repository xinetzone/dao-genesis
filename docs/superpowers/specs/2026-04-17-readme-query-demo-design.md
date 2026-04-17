# README 查询演示（遵循 Contract）设计文档

## 背景
当前仓库已在 `src/system-prompt.md` 中落地 `# Contract (Strict)`，明确了：
- 工具白名单：`Glob`、`Grep`、`Read`、`Write`
- 查询输出契约：Top N=3、每条仅 `review_id + 核心结论 + 行动`，禁止输出完整 JSON
- 查询读取硬阈值：最多读取 3 个文件、每个文件最多 120 行片段

为降低上手成本与提高可验收性，需要在 README 中补充一段“查询演示”，让读者既能看到用户指令与期望输出，也能看到内部工具调用顺序（用于调试与对齐 Contract）。

## 目标
- 在 README 增加一个可复制的查询演示段落（用户指令 + 期望输出模板）
- 明确内部工具流程：`Glob → Grep → Read`
- 明确查询硬阈值与禁止项，避免输出完整 JSON 或冗长原文

## 范围
### In Scope
- 修改 `README.md`：新增 `### 查询演示（遵循 Contract）` 小节
- 演示仅覆盖“查询”场景（不覆盖写入/更新）

### Out of Scope
- 新增可执行脚本（本次只交付 README 步骤）
- 修改 `src/system-prompt.md` 或 `src/memory-schema.json`

## 设计
### 放置位置
放在 README 的 `## 💬 使用示例 (Usage Examples)` 之后（紧邻现有示例，便于读者连续阅读）。

### 小节结构
1. 用户指令示例（1 个）
2. 内部工具流程（按顺序描述目的）
3. 读取硬阈值（与 Contract 保持一致）
4. 期望输出模板（Top N=3）
5. 禁止项（输出完整 JSON、输出整段原文）

### 文案草案（将直接用于 README）

```text
### 查询演示（遵循 Contract）

用户指令示例：
> @dao-genesis 查询记忆：schema 扁平化 工具白名单

内部工具流程（用于调试与对齐 Contract）：
1) Glob：定位候选文件（.storage/reviews/REV-*.json）
2) Grep：用关键词初筛命中记录（必要时拆分多个关键词）
3) Read：仅读取少量命中文件片段以提炼“核心结论/行动项”

读取硬阈值：
- 最多读取 3 个文件
- 每个文件最多读取 120 行片段（必要时用 offset/limit）

期望输出（Top N=3，极简返回）：
- REV-20260417-002 | 核心结论：Schema 扁平化降低写入难度 | 行动：统一工具白名单并补齐极简输出模板

禁止：
- 输出完整 JSON
- 输出整段原文/整份复盘报告
```

## 验收标准
- README 中新增的小节包含：用户指令、工具流程、硬阈值、输出模板、禁止项
- 输出模板符合 `src/system-prompt.md` 的 Query Output Contract（Top N=3、每条三段式）
- 文案不诱导用户索取或展示完整 JSON
