import os
from datetime import datetime
from jinja2 import Template

# 导入之前实现的模块
from trigger import ReviewTrigger
from error_collector import ErrorCollector, global_error_collector
from task_tracker import TaskTracker
from goal_issue_tracker import GoalIssueTracker
from suggestion_generator import SuggestionGenerator
from graphql_client import global_graphql_client

class ReviewAutomation:
    def __init__(self):
        self.config = self.load_config()
        self.template_path = os.path.join(os.path.dirname(__file__), 'review-template.md')
        
        # 确保输出目录存在
        os.makedirs(self.config['review_output_dir'], exist_ok=True)
    
    def load_config(self):
        """加载配置"""
        config = global_graphql_client.get_config()
        if config:
            return {
                'review_output_dir': config.get('review_output_dir', './reviews'),
                'task_data_dir': config.get('task_data_dir', './data/tasks'),
                'error_log_dir': config.get('error_log_dir', './logs/errors')
            }
        return {
            'review_output_dir': './reviews',
            'task_data_dir': './data/tasks',
            'error_log_dir': './logs/errors'
        }
    
    def generate_review_id(self):
        """生成复盘ID"""
        date_str = datetime.now().strftime('%Y%m%d')
        # 生成3位随机数
        import random
        random_str = f"{random.randint(0, 999):03d}"
        return f"REV-{date_str}-{random_str}"
    
    def load_template(self):
        """加载模板文件"""
        if os.path.exists(self.template_path):
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return Template(f.read())
        else:
            # 如果模板文件不存在，使用默认模板
            default_template = """
---
title: 任务复盘记录
date: {{date}}
task_type: {{task_type}}
trigger_type: {{trigger_type}}
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
| {{goal.name}} | {{goal.metric}} | {{goal.actual}}/{{goal.target}} |
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
            """
            return Template(default_template)
    
    def collect_data(self):
        """收集复盘所需的数据"""
        # 收集错误和异常信息
        error_collector = ErrorCollector()
        # 尝试加载最新的错误数据
        error_collector.get_errors()
        error_collector.get_exceptions()
        
        errors = error_collector.get_errors()
        exceptions = error_collector.get_exceptions()
        
        # 收集任务完成情况
        task_tracker = TaskTracker()
        task_tracker.get_all_tasks()
        task_stats = task_tracker.get_completion_stats()
        tasks = task_tracker.get_all_tasks()
        
        # 收集目标和问题
        goal_issue_tracker = GoalIssueTracker()
        goal_issue_tracker.get_goals()
        goal_issue_tracker.get_issues()
        goals = goal_issue_tracker.get_achieved_goals()
        issues = goal_issue_tracker.get_open_issues()
        
        # 生成改进建议
        suggestion_generator = SuggestionGenerator()
        suggestions = suggestion_generator.generate_suggestions(
            task_stats=task_stats,
            errors=errors,
            exceptions=exceptions,
            issues=issues
        )
        
        return {
            'errors': errors,
            'exceptions': exceptions,
            'task_stats': task_stats,
            'tasks': tasks,
            'goals': goals,
            'issues': issues,
            'suggestions': suggestions
        }
    
    def generate_review(self, task_type, trigger_type, trigger_details):
        """生成复盘记录"""
        # 收集数据
        data = self.collect_data()
        
        # 准备模板数据
        template_data = {
            'review_id': self.generate_review_id(),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'datetime': datetime.now().isoformat(),
            'task_type': task_type,
            'trigger_type': trigger_type,
            'trigger_details': trigger_details,
            'errors': data['errors'],
            'exception_stack': '\n'.join([e['stack'] for e in data['exceptions']]) if data['exceptions'] else '无',
            'progress_percentage': round(data['task_stats'].get('progress_percentage', 0), 2),
            'completed_items': data['task_stats'].get('completed', 0),
            'pending_items': data['task_stats'].get('pending', 0) + data['task_stats'].get('in_progress', 0),
            'tasks': data['tasks'],
            'goals': data['goals'],
            'issues': data['issues'],
            'process_suggestions': data['suggestions'].get('process', []),
            'efficiency_suggestions': data['suggestions'].get('efficiency', []),
            'quality_suggestions': data['suggestions'].get('quality', []),
            'summary': self.generate_summary(data)
        }
        
        # 加载模板
        template = self.load_template()
        
        # 生成Markdown内容
        markdown_content = template.render(**template_data)
        
        # 保存复盘记录
        filename = f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        output_path = os.path.join(self.config['review_output_dir'], filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return output_path
    
    def generate_summary(self, data):
        """生成复盘总结"""
        task_stats = data['task_stats']
        error_count = len(data['errors'])
        exception_count = len(data['exceptions'])
        achieved_goals = len(data['goals'])
        open_issues = len(data['issues'])
        
        summary = f"本次复盘覆盖了 {task_stats.get('total', 0)} 个任务，完成率 {round(task_stats.get('progress_percentage', 0), 2)}%。"
        
        if error_count > 0:
            summary += f" 发生了 {error_count} 个错误和 {exception_count} 个异常。"
        else:
            summary += " 未发生错误和异常。"
        
        if achieved_goals > 0:
            summary += f" 已达成 {achieved_goals} 个目标。"
        
        if open_issues > 0:
            summary += f" 存在 {open_issues} 个未解决的问题。"
        
        summary += " 请参考改进建议部分，优化后续执行流程。"
        
        return summary
    
    def run(self, task_type, trigger_type='manual', trigger_details='手动触发'):
        """运行复盘流程"""
        print(f"开始执行复盘流程...")
        print(f"任务类型: {task_type}")
        print(f"触发类型: {trigger_type}")
        print(f"触发详情: {trigger_details}")
        
        try:
            output_path = self.generate_review(task_type, trigger_type, trigger_details)
            print(f"\n复盘记录已生成: {output_path}")
            return output_path
        except Exception as e:
            print(f"\n执行复盘流程时发生错误: {str(e)}")
            # 记录错误
            global_error_collector.record_exception(e, {'context': 'review_automation'})
            return None

if __name__ == "__main__":
    # 示例用法
    automation = ReviewAutomation()
    
    # 运行复盘流程
    output_path = automation.run(
        task_type='daily_review',
        trigger_type='scheduled',
        trigger_details='每日定期触发'
    )
    
    if output_path:
        print(f"\n复盘记录内容:")
        with open(output_path, 'r', encoding='utf-8') as f:
            print(f.read())