# 任务复盘机制使用指南

## 1. 概述

任务复盘机制是一个系统化的工具，用于记录和分析任务执行过程中的关键信息，支持定期和不定期触发方式，并提供多维度检索能力。

### 主要功能

- **定期触发复盘**：支持每日、每周固定时间自动触发
- **不定期触发复盘**：支持在任务关键节点、异常发生后自动触发
- **结构化记录**：记录错误信息、异常堆栈、任务完成情况、已达成目标、未解决问题、改进建议
- **自动化处理**：使用Python 3.14编写脚本实现自动化处理
- **标准化存储**：以MyST Markdown格式进行标准化存储
- **多维度检索**：支持按时间范围、任务类型、错误类型等多维度检索

## 2. 安装与配置

### 2.1 安装依赖

```bash
pip install schedule jinja2 requests
```

### 2.2 配置管理

系统配置通过 GraphQL 服务管理，不再使用本地配置文件。配置项包括：

- `scheduled_triggers`：定期触发规则
- `review_output_dir`：复盘记录存储目录
- `error_log_dir`：错误日志存储目录
- `task_data_dir`：任务数据存储目录

配置可通过系统 API 进行管理，详细请参考 GraphQL API 文档。

## 3. 使用方法

### 3.1 命令行接口

复盘机制提供了完整的命令行接口，通过 `review_system.py` 脚本使用：

#### 启动触发服务

```bash
python src/review_system.py start
```

#### 停止触发服务

```bash
python src/review_system.py stop
```

#### 运行复盘流程

```bash
python src/review_system.py run <task_type> [--trigger-type <type>] [--trigger-details <details>]
```

#### 检索复盘记录

```bash
python src/review_system.py search [--start-time <time>] [--end-time <time>] [--task-type <type>] [--error-code <code>]
```

#### 添加定期触发规则

```bash
python src/review_system.py add-trigger <time> <recurrence> <task_type> [--day <day>]
```

#### 列出定期触发规则

```bash
python src/review_system.py list-triggers
```

#### 触发基于事件的复盘

```bash
python src/review_system.py event-trigger <task_type> <event_type> <event_details>
```

#### 显示系统状态

```bash
python src/review_system.py status
```

### 3.2 集成到现有系统

#### 方式一：直接调用API

```python
from src.review_system import ReviewSystem

# 初始化系统
system = ReviewSystem()

# 运行复盘
system.run_review('task_type', 'trigger_type', 'trigger_details')

# 搜索复盘记录
system.search_reviews(start_time, end_time, task_type, error_code)

# 触发基于事件的复盘
system.trigger_event_review('task_type', 'event_type', 'event_details')
```

#### 方式二：使用错误捕获装饰器

```python
from src.error_collector import error_catcher, error_catching

# 使用装饰器
@error_catcher
def my_function():
    # 函数代码
    pass

# 使用上下文管理器
with error_catching({'context': 'test'}):
    # 代码块
    pass
```

## 4. 复盘记录格式

复盘记录以MyST Markdown格式存储，包含以下部分：

- **基本信息**：复盘ID、日期时间、任务类型、触发类型、触发详情
- **错误信息**：错误代码、描述文本、发生时间
- **异常堆栈跟踪**：完整的异常堆栈信息
- **任务完成情况**：总进度、已完成项、未完成项、任务明细
- **已达成目标**：目标、衡量指标、达成情况
- **未解决问题**：问题、当前状态、影响、优先级
- **改进建议**：流程方面、效率方面、质量方面
- **总结**：复盘总结

## 5. 目录结构

```
dao-genesis/
├── src/
│   ├── trigger.py                  # 触发机制
│   ├── error_collector.py          # 错误和异常信息收集
│   ├── task_tracker.py             # 任务完成情况记录
│   ├── goal_issue_tracker.py       # 目标达成和问题记录
│   ├── suggestion_generator.py     # 改进建议生成
│   ├── review_automation.py        # 自动化处理脚本
│   ├── review_search.py            # 多维度检索接口
│   ├── review_system.py            # 主系统脚本
│   ├── graphql_client.py           # GraphQL客户端
│   ├── graphql_schema.py           # GraphQL模式定义
│   ├── graphql_server_app.py       # GraphQL服务器应用
│   └── review-template.md          # 复盘记录模板
├── reviews/                        # 复盘记录存储目录
├── logs/                           # 日志存储目录
│   └── errors/                     # 错误日志存储目录
├── data/                           # 数据存储目录
│   └── tasks/                      # 任务数据存储目录
└── docs/                           # 文档目录
    └── review-mechanism.md         # 使用指南
```

## 6. 示例

### 6.1 运行每日复盘

```bash
python src/review_system.py run daily_review --trigger-type scheduled --trigger-details "每日定期触发"
```

### 6.2 搜索特定任务类型的复盘记录

```bash
python src/review_system.py search --task-type daily_review
```

### 6.3 添加每周五的复盘触发

```bash
python src/review_system.py add-trigger 17:00 weekly weekly_review --day friday
```

## 7. 故障排除

### 7.1 常见问题

1. **触发服务无法启动**
   - 检查schedule库是否安装：`pip install schedule`
   - 检查GraphQL服务是否正常运行

2. **复盘记录生成失败**
   - 检查jinja2库是否安装：`pip install jinja2`
   - 检查输出目录是否存在且有写入权限

3. **检索功能无法正常工作**
   - 检查复盘记录目录是否存在
   - 检查复盘记录文件格式是否正确

4. **GraphQL相关错误**
   - 检查requests库是否安装：`pip install requests`
   - 检查GraphQL服务地址配置是否正确

### 7.2 日志查看

错误日志存储在 `logs/errors/` 目录中，可通过查看日志文件了解系统运行情况。

## 8. 最佳实践

1. **定期维护**：定期检查触发规则和系统状态
2. **合理配置**：根据实际需求配置触发规则和存储路径
3. **及时分析**：定期分析复盘记录，发现问题并及时改进
4. **集成使用**：将复盘机制集成到现有任务执行流程中，形成完整的闭环

## 9. 版本历史

- **v1.1**：配置系统升级，从本地配置文件迁移到GraphQL服务管理
- **v1.0**：初始版本，实现了基本的复盘机制功能