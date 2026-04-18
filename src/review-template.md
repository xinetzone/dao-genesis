---
title: 任务复盘记录
date: {{date}}
task_type: {{task_type}}
trigger_type: {{trigger_type}}  # scheduled 或 event-based
trigger_details: {{trigger_details}}
---

# 任务复盘记录

## 基本信息

- **复盘ID**: {{review_id}}
- **日期时间**: {{datetime}}
- **任务类型**: {{task_type}}
- **触发类型**: {{trigger_type}}
- **触发详情**: {{trigger_details}}

## 错误信息

| 错误代码 | 描述文本 | 发生时间 |
|---------|---------|--------|
{% for error in errors %}
| {{error.code}} | {{error.message}} | {{error.timestamp}} |
{% endfor %}

## 异常堆栈跟踪

```
{{exception_stack}}
```

## 任务完成情况

- **总进度**: {{progress_percentage}}%
- **已完成项**: {{completed_items}}
- **未完成项**: {{pending_items}}

### 任务明细

| 任务项 | 状态 | 完成时间 |
|-------|------|--------|
{% for task in tasks %}
| {{task.name}} | {{task.status}} | {{task.completed_at or 'N/A'}} |
{% endfor %}

## 已达成目标

| 目标 | 衡量指标 | 达成情况 |
|-----|---------|--------|
{% for goal in goals %}
| {{goal.name}} | {{goal.metric}} | {{goal.achievement}} |
{% endfor %}

## 未解决问题

| 问题 | 当前状态 | 影响 | 优先级 |
|-----|---------|------|-------|
{% for issue in issues %}
| {{issue.description}} | {{issue.status}} | {{issue.impact}} | {{issue.priority}} |
{% endfor %}

## 改进建议

### 流程方面

{% for suggestion in process_suggestions %}
- {{suggestion}}
{% endfor %}

### 效率方面

{% for suggestion in efficiency_suggestions %}
- {{suggestion}}
{% endfor %}

### 质量方面

{% for suggestion in quality_suggestions %}
- {{suggestion}}
{% endfor %}

## 总结

{{summary}}