# inject_memory 自动归一化（Markdown 解析增强）设计文档

## 背景
当前 [inject_memory.py](file:///workspace/scripts/inject_memory.py) 对数组字段仅支持 `- item` / `* item` 形式的列表项提取，无法覆盖常见的编号/符号/括号等写法，导致“本地 Markdown → JSON”注入链路对输入格式过于敏感。

## 目标
- 在保持“严格静默执行”的前提下，增强数组字段的条目识别能力，自动归一化常见条目写法为统一的列表项文本。
- 不改变 JSON Schema 与校验规则（仍需通过 [validate_reviews.py](file:///workspace/scripts/validate_reviews.py)）。

## 范围
### In Scope
- 修改 [inject_memory.py](file:///workspace/scripts/inject_memory.py)：为数组字段新增“自动归一化”提取逻辑。
- 增加一个回归用 Markdown 输入样例，并验证生成 JSON 可通过校验脚本。

### Out of Scope
- 交互式补全缺失字段
- 更复杂的 Markdown AST 解析（不引入第三方库）
- 段落内容/嵌套列表的语义合并（后续迭代）

## 设计
### 条目识别（按优先级）
在数组字段（participants/decisions/success_factors/failure_reasons/best_practices/action_items）下，将以下行识别为条目并抽取正文：
- 无序列表：`- xxx`、`* xxx`
- 编号列表：`1. xxx`、`1) xxx`
- 中文括号编号：`（1）xxx`
- 圈号编号：`① xxx`（或 `①xxx`）
- 符号点：`• xxx`、`· xxx`
- 括号包裹：`【xxx】`、`[xxx]`（整行作为正文）

### 归一化规则
- 去除条目前缀（符号/编号/括号编号/点符号）
- `strip()` 清理两侧空格
- 若归一化后为空字符串则丢弃
- 不拆分正文内部的全角/半角冒号（如 `：`），作为正文保留

### 实现形态
- 在 `parse_markdown()` 中对数组字段的行解析统一调用 `normalize_bullet_line(line) -> str | None`
- 新增 `normalize_bullet_line()`（纯标准库实现），集中维护 regex 规则，便于未来扩展

## 验收标准
- 对同一数组字段，以下输入均能被识别为条目并写入 JSON：
  - `- xxx`、`1. xxx`、`（1）xxx`、`① xxx`、`• xxx`、`【xxx】`
- 生成的记录能通过 [validate_reviews.py](file:///workspace/scripts/validate_reviews.py) 校验
- 运行过程保持静默（不进入交互，不要求补全字段）
