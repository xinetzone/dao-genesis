# Memory Management Script Implementation Plan

## 目标
根据设计文档，实现 `scripts/manage_memory.py` 脚本，支持更新与归档历史复盘记录。

## 实施步骤
### 1. 脚本编写 (`scripts/manage_memory.py`)
- [x] 创建基础框架，配置 `argparse` 子命令 `update` 和 `archive`。
- [x] 实现 `load_record` 和 `save_record`。
- [x] 实现 `archive` 命令逻辑：将 `status` 字段修改为 `"archived"`，成功后输出 `[<review_id>] 归档成功`。
- [x] 实现 `update` 命令逻辑：
  - 检查待修改字段是否合法。
  - 支持对数组类型的 `--append` 追加（输出为 `[新增] <新值>`）。
  - 支持对普通类型或数组的直接覆盖（输出为 `[修改] <新值>`）。
  - 严格遵守 `src/system-prompt.md` 中的输出契约。

### 2. 编写单元测试 (`tests/test_manage_memory.py`)
- [x] 测试 `archive` 对新记录、已归档记录的影响及输出格式。
- [x] 测试 `update` 对字符串类型（覆盖）的修改。
- [x] 测试 `update` 对数组类型追加 (`--append`) 的影响。
- [x] 验证错误处理（如找不到对应的 `review_id`）。

### 3. 测试与集成 (`scripts/run_tests.sh`)
- [x] 运行所有单元测试，确保 `test_manage_memory.py` 通过。
- [x] 确保生成的记录依然能够通过 `scripts/validate_reviews.py` 校验。

### 4. 文档更新 (`README.md`)
- [x] 在 `README.md` 的适当位置补充管理脚本（Update / Archive）的 CLI 示例，对齐之前注入工具的格式。
