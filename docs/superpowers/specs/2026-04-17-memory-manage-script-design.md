# 记忆管理本地脚本 (Update & Archive) 设计文档

## 背景
当前 `src/system-prompt.md` 已经定义了明确的 `Update Output Contract` 和 `Archive Output Contract`，但是项目中只提供了创建记录的脚本（`scripts/inject_memory.py`），缺少针对已有记录进行更新与归档的本地命令行工具。这导致通过终端或自动化脚本管理历史复盘记录时操作不便，容易破坏 JSON 结构。

## 目标
- 开发一个本地 Python 脚本（如 `scripts/manage_memory.py`）支持对 `.storage/reviews/` 下的复盘记录进行字段更新与状态归档。
- 该脚本的命令行输出必须严格对齐 System Prompt 中的契约（仅返回变更差异或归档成功提示，禁止打印完整 JSON）。
- 保证更新后的 JSON 依然符合 `src/memory-schema.json`，且能通过 `validate_reviews.py` 校验。

## 范围
### In Scope
- 新增 `scripts/manage_memory.py` 脚本，包含两个子命令：`update` 和 `archive`。
- 增加对应单元测试。
- 更新 README 以补充本地管理指令示例。

### Out of Scope
- 批量更新/归档多个文件。
- 复杂的 JSON 结构重构（当前仅针对扁平化 schema 字段做一维更新/追加）。

## 设计

### 命令行接口设计
使用 `argparse` 提供子命令结构。

#### 1. Update 命令
```bash
python scripts/manage_memory.py update <review_id> --field <field_name> --value <new_value> [--append]
```
- `review_id`：目标复盘记录 ID（例如 `REV-20260417-001`）。
- `--field`：要修改的字段名（如 `action_items`、`task_type` 等）。
- `--value`：新的字段值。
- `--append`：可选标志，当且仅当目标字段为数组类型（如 `decisions`, `action_items` 等）时，执行“追加”操作而不是“覆盖”。如果未传该标志，默认覆盖。

**输出契约对齐：**
- 成功：
  ```
  [REV-20260417-001]
  action_items: [新增] 增加 Redis 缓存层
  ```
- 失败：抛出简洁错误提示。

#### 2. Archive 命令
```bash
python scripts/manage_memory.py archive <review_id>
```
- 行为：将目标 JSON 中的 `status` 字段修改为 `"archived"`。

**输出契约对齐：**
- 成功：`[REV-20260417-001] 归档成功`

### 内部实现逻辑
- `load_record(review_id)`：根据 `review_id` 从 `.storage/reviews/` 读取 JSON 文件。若不存在则报错退出。
- `save_record(review_id, data)`：将更新后的数据以美化的 JSON 格式安全地写回文件，注意保持 UTF-8 编码。
- **更新处理 (Update)**：
  - 验证字段名是否合法（是否在 schema 允许范围内，可选读取 `src/memory-schema.json` 或写死常见字段）。
  - 若为数组字段且携带 `--append`，将 `--value` 加入数组末尾；否则替换原有值（若是数组字段覆盖，可按约定接收单个值或逗号分隔的值，这里以覆盖整个字段或处理单条为主，建议简单起见，`--value` 作为新值）。
- **归档处理 (Archive)**：
  - 若 `status` 已经是 `archived`，则无需修改，直接返回成功。否则更新为 `archived`。

## 验收标准
1. 使用 `update` 追加一条 `action_items`，输出格式符合 `action_items: [新增] ...`。
2. 使用 `archive` 归档一个文件，输出为 `[REV-xxx] 归档成功`，且 JSON 中的 `status` 变为 `archived`。
3. 执行后，`validate_reviews.py` 校验全部通过。
