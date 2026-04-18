import os
from datetime import datetime
from graphql_client import global_graphql_client

class SuggestionGenerator:
    def __init__(self):
        self.config = self.load_config()
        self.suggestions = {
            'process': [],
            'efficiency': [],
            'quality': []
        }
    
    def load_config(self):
        """加载配置"""
        config = global_graphql_client.get_config()
        if config:
            return {
                'task_data_dir': config.get('task_data_dir', './data/tasks'),
                'review_output_dir': config.get('review_output_dir', './reviews'),
                'error_log_dir': config.get('error_log_dir', './logs/errors')
            }
        return {
            'task_data_dir': './data/tasks',
            'review_output_dir': './reviews',
            'error_log_dir': './logs/errors'
        }
    
    def generate_suggestions(self, task_stats=None, errors=None, exceptions=None, issues=None):
        """生成改进建议"""
        # 清空现有建议
        self.suggestions = {
            'process': [],
            'efficiency': [],
            'quality': []
        }
        
        # 基于任务完成情况生成建议
        if task_stats:
            self._generate_task_based_suggestions(task_stats)
        
        # 基于错误和异常生成建议
        if errors or exceptions:
            self._generate_error_based_suggestions(errors, exceptions)
        
        # 基于问题记录生成建议
        if issues:
            self._generate_issue_based_suggestions(issues)
        
        # 保存建议到GraphQL
        for suggestion_type, suggestion_list in self.suggestions.items():
            for content in suggestion_list:
                global_graphql_client.add_suggestion(suggestion_type, content)
        
        return self.suggestions
    
    def _generate_task_based_suggestions(self, task_stats):
        """基于任务完成情况生成建议"""
        progress = task_stats.get('progress_percentage', 0)
        pending_tasks = task_stats.get('pending', 0)
        in_progress_tasks = task_stats.get('in_progress', 0)
        
        if progress < 50:
            self.suggestions['efficiency'].append('任务进度较慢，建议优先处理高优先级任务，合理分配资源')
            self.suggestions['process'].append('检查任务依赖关系，确保关键路径任务得到及时处理')
        
        if pending_tasks > task_stats.get('total', 0) * 0.5:
            self.suggestions['process'].append('待处理任务过多，建议重新评估任务优先级和截止日期')
        
        if in_progress_tasks > task_stats.get('total', 0) * 0.3:
            self.suggestions['process'].append('进行中任务过多，可能导致资源分散，建议聚焦关键任务')
    
    def _generate_error_based_suggestions(self, errors, exceptions):
        """基于错误和异常生成建议"""
        error_count = len(errors) if errors else 0
        exception_count = len(exceptions) if exceptions else 0
        
        if error_count > 5:
            self.suggestions['quality'].append('错误数量较多，建议加强代码审查和测试')
            self.suggestions['process'].append('建立错误分类和跟踪机制，优先解决高频错误')
        
        if exception_count > 3:
            self.suggestions['quality'].append('异常数量较多，建议加强异常处理和边界情况测试')
            self.suggestions['process'].append('分析异常类型，制定相应的预防措施')
        
        # 分析错误类型
        error_codes = {}  
        if errors:
            for error in errors:
                code = error.get('code', 'Unknown')
                error_codes[code] = error_codes.get(code, 0) + 1
            
            # 找出高频错误
            for code, count in error_codes.items():
                if count > 2:
                    self.suggestions['quality'].append(f'错误代码 {code} 出现频率较高，建议重点排查和修复')
    
    def _generate_issue_based_suggestions(self, issues):
        """基于问题记录生成建议"""
        open_issues = [issue for issue in issues if issue['status'] in ['open', 'in_progress']]
        high_priority_issues = [issue for issue in issues if issue['priority'] in ['high', 'critical']]
        
        if len(open_issues) > 5:
            self.suggestions['process'].append('未解决问题较多，建议召开问题分析会议，制定解决方案')
        
        if len(high_priority_issues) > 2:
            self.suggestions['process'].append('高优先级问题较多，建议优先分配资源解决')
        
        # 分析问题影响
        impact_counts = {}
        for issue in issues:
            impact = issue.get('impact', 'Unknown')
            impact_counts[impact] = impact_counts.get(impact, 0) + 1
        
        for impact, count in impact_counts.items():
            if count > 2:
                self.suggestions['process'].append(f'影响 "{impact}" 的问题较多，建议从根本原因入手解决')
    
    def get_suggestions(self):
        """获取所有建议"""
        # 从GraphQL获取最新建议
        suggestions_data = global_graphql_client.get_suggestions()
        # 按类型分组
        self.suggestions = {
            'process': [],
            'efficiency': [],
            'quality': []
        }
        for suggestion in suggestions_data:
            if suggestion['type'] in self.suggestions:
                self.suggestions[suggestion['type']].append(suggestion['content'])
        return self.suggestions
    
    def save_suggestions(self, filename=None):
        """保存建议（已迁移到GraphQL，此方法保留以保持兼容性）"""
        # 建议已通过GraphQL存储，此方法保留以保持API兼容性
        return "Suggestions stored in GraphQL"
    
    def load_suggestions(self, filename):
        """加载建议（已迁移到GraphQL，此方法保留以保持兼容性）"""
        # 建议已通过GraphQL存储，此方法保留以保持API兼容性
        # 从GraphQL获取最新建议
        self.get_suggestions()
        return True
    
    def clear_suggestions(self):
        """清除所有建议"""
        self.suggestions = {
            'process': [],
            'efficiency': [],
            'quality': []
        }

if __name__ == "__main__":
    # 示例用法
    generator = SuggestionGenerator()
    
    # 模拟任务统计数据
    task_stats = {
        'total': 10,
        'completed': 3,
        'pending': 5,
        'in_progress': 2,
        'progress_percentage': 30
    }
    
    # 模拟错误数据
    errors = [
        {'code': 'E001', 'message': '测试错误1'},
        {'code': 'E001', 'message': '测试错误2'},
        {'code': 'E002', 'message': '测试错误3'},
        {'code': 'E001', 'message': '测试错误4'},
        {'code': 'E003', 'message': '测试错误5'},
        {'code': 'E003', 'message': '测试错误6'}
    ]
    
    # 模拟异常数据
    exceptions = [
        {'type': 'ZeroDivisionError', 'message': 'division by zero'},
        {'type': 'ValueError', 'message': 'invalid value'},
        {'type': 'RuntimeError', 'message': 'runtime error'}
    ]
    
    # 模拟问题数据
    issues = [
        {'description': '任务进度缓慢', 'impact': '项目延期', 'priority': 'high', 'status': 'in_progress'},
        {'description': '资源不足', 'impact': '多个任务受阻', 'priority': 'high', 'status': 'open'},
        {'description': '技术难题', 'impact': '任务无法推进', 'priority': 'medium', 'status': 'open'},
        {'description': '沟通不畅', 'impact': '任务理解偏差', 'priority': 'medium', 'status': 'open'},
        {'description': '文档不全', 'impact': '开发效率低', 'priority': 'low', 'status': 'open'},
        {'description': '测试覆盖不足', 'impact': '质量问题', 'priority': 'medium', 'status': 'open'}
    ]
    
    # 生成建议
    suggestions = generator.generate_suggestions(task_stats, errors, exceptions, issues)
    
    # 打印建议
    print("生成的改进建议:")
    print("\n流程方面:")
    for suggestion in suggestions['process']:
        print(f"- {suggestion}")
    
    print("\n效率方面:")
    for suggestion in suggestions['efficiency']:
        print(f"- {suggestion}")
    
    print("\n质量方面:")
    for suggestion in suggestions['quality']:
        print(f"- {suggestion}")
    
    # 保存建议
    saved_file = generator.save_suggestions()
    print(f"\n建议保存到: {saved_file}")