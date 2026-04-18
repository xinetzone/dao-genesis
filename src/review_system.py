import argparse
import os
from datetime import datetime

# 导入之前实现的模块
from trigger import ReviewTrigger
from review_automation import ReviewAutomation
from review_search import ReviewSearch
from error_collector import ErrorCollector
from task_tracker import TaskTracker
from goal_issue_tracker import GoalIssueTracker
from suggestion_generator import SuggestionGenerator
from graphql_client import global_graphql_client

class ReviewSystem:
    def __init__(self):
        self.config = self.load_config()
        self.trigger = ReviewTrigger()
        self.automation = ReviewAutomation()
        self.searcher = ReviewSearch()
    
    def load_config(self):
        """加载配置"""
        config = global_graphql_client.get_config()
        if config:
            return {
                'review_output_dir': config.get('review_output_dir', './reviews'),
                'task_data_dir': config.get('task_data_dir', './data/tasks'),
                'error_log_dir': config.get('error_log_dir', './logs/errors'),
                'scheduled_triggers': [
                    {
                        'time': t['time'],
                        'recurrence': t['recurrence'],
                        'task_type': t['task_type'],
                        'day': t.get('day')
                    } for t in config.get('scheduled_triggers', [])
                ]
            }
        return {
            'review_output_dir': './reviews',
            'task_data_dir': './data/tasks',
            'error_log_dir': './logs/errors',
            'scheduled_triggers': [
                {'time': '08:00', 'recurrence': 'daily', 'task_type': 'daily_review'},
                {'time': '09:00', 'recurrence': 'weekly', 'day': 'monday', 'task_type': 'weekly_review'}
            ]
        }
    
    def start_trigger_service(self):
        """启动触发服务"""
        print("启动复盘触发服务...")
        self.trigger.start()
        print("复盘触发服务已启动")
    
    def stop_trigger_service(self):
        """停止触发服务"""
        print("停止复盘触发服务...")
        self.trigger.stop()
        print("复盘触发服务已停止")
    
    def run_review(self, task_type, trigger_type='manual', trigger_details='手动触发'):
        """运行复盘流程"""
        return self.automation.run(task_type, trigger_type, trigger_details)
    
    def search_reviews(self, start_time=None, end_time=None, task_type=None, error_code=None):
        """检索复盘记录"""
        results = self.searcher.search(start_time, end_time, task_type, error_code)
        self.searcher.display_results(results)
        return results
    
    def add_scheduled_trigger(self, time_str, recurrence, task_type, day=None):
        """添加定期触发规则"""
        self.trigger.add_scheduled_trigger(time_str, recurrence, task_type, day)
        print(f"已添加定期触发规则: {recurrence} at {time_str} for {task_type}")
    
    def list_scheduled_triggers(self):
        """列出所有定期触发规则"""
        triggers = self.trigger.config.get('scheduled_triggers', [])
        print("定期触发规则:")
        for i, trigger in enumerate(triggers, 1):
            if trigger['recurrence'] == 'weekly':
                print(f"{i}. {trigger['day']} at {trigger['time']} - {trigger['task_type']}")
            else:
                print(f"{i}. Daily at {trigger['time']} - {trigger['task_type']}")
    
    def trigger_event_review(self, task_type, event_type, event_details):
        """触发基于事件的复盘"""
        print(f"触发基于事件的复盘: {event_type}")
        self.trigger.trigger_event_based_review(task_type, event_type, event_details)
    
    def display_status(self):
        """显示系统状态"""
        print("系统状态:")
        print(f"复盘记录目录: {self.config.get('review_output_dir', './reviews')}")
        print(f"任务数据目录: {self.config.get('task_data_dir', './data/tasks')}")
        print(f"错误日志目录: {self.config.get('error_log_dir', './logs/errors')}")
        
        # 统计复盘记录数量
        review_dir = self.config.get('review_output_dir', './reviews')
        if os.path.exists(review_dir):
            review_files = [f for f in os.listdir(review_dir) if f.startswith('review_') and f.endswith('.md')]
            print(f"复盘记录数量: {len(review_files)}")
        else:
            print("复盘记录目录不存在")
        
        # 统计任务数量
        task_tracker = TaskTracker()
        task_tracker.get_all_tasks()
        task_stats = task_tracker.get_completion_stats()
        print(f"任务总数: {task_stats.get('total', 0)}")
        print(f"已完成任务: {task_stats.get('completed', 0)}")
        print(f"进行中任务: {task_stats.get('in_progress', 0)}")
        print(f"待处理任务: {task_stats.get('pending', 0)}")
        print(f"任务完成率: {task_stats.get('progress_percentage', 0):.2f}%")

def get_version():
    """获取版本信息"""
    try:
        from pdm.version import get_version
        return get_version()
    except ImportError:
        try:
            import importlib.metadata
            return importlib.metadata.version("dao-review-system")
        except importlib.metadata.PackageNotFoundError:
            return "0.0.0"

def main():
    parser = argparse.ArgumentParser(description='任务复盘系统')

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # 版本信息
    version_parser = subparsers.add_parser('version', help='显示版本信息')
    
    # 启动触发服务
    start_parser = subparsers.add_parser('start', help='启动复盘触发服务')
    
    # 停止触发服务
    stop_parser = subparsers.add_parser('stop', help='停止复盘触发服务')
    
    # 运行复盘
    run_parser = subparsers.add_parser('run', help='运行复盘流程')
    run_parser.add_argument('task_type', help='任务类型')
    run_parser.add_argument('--trigger-type', default='manual', help='触发类型')
    run_parser.add_argument('--trigger-details', default='手动触发', help='触发详情')
    
    # 搜索复盘记录
    search_parser = subparsers.add_parser('search', help='检索复盘记录')
    search_parser.add_argument('--start-time', help='开始时间 (YYYY-MM-DD HH:MM:SS)')
    search_parser.add_argument('--end-time', help='结束时间 (YYYY-MM-DD HH:MM:SS)')
    search_parser.add_argument('--task-type', help='任务类型')
    search_parser.add_argument('--error-code', help='错误代码')
    
    # 添加定期触发规则
    add_trigger_parser = subparsers.add_parser('add-trigger', help='添加定期触发规则')
    add_trigger_parser.add_argument('time', help='触发时间 (HH:MM)')
    add_trigger_parser.add_argument('recurrence', choices=['daily', 'weekly'], help='触发频率')
    add_trigger_parser.add_argument('task_type', help='任务类型')
    add_trigger_parser.add_argument('--day', help='星期几 (仅用于weekly)')
    
    # 列出定期触发规则
    list_triggers_parser = subparsers.add_parser('list-triggers', help='列出所有定期触发规则')
    
    # 触发基于事件的复盘
    event_trigger_parser = subparsers.add_parser('event-trigger', help='触发基于事件的复盘')
    event_trigger_parser.add_argument('task_type', help='任务类型')
    event_trigger_parser.add_argument('event_type', help='事件类型')
    event_trigger_parser.add_argument('event_details', help='事件详情')
    
    # 显示系统状态
    status_parser = subparsers.add_parser('status', help='显示系统状态')
    
    args = parser.parse_args()
    
    system = ReviewSystem()
    
    if args.command == 'start':
        system.start_trigger_service()
    elif args.command == 'stop':
        system.stop_trigger_service()
    elif args.command == 'run':
        system.run_review(args.task_type, args.trigger_type, args.trigger_details)
    elif args.command == 'search':
        # 解析时间参数
        start_time = None
        end_time = None
        if args.start_time:
            start_time = datetime.strptime(args.start_time, '%Y-%m-%d %H:%M:%S')
        if args.end_time:
            end_time = datetime.strptime(args.end_time, '%Y-%m-%d %H:%M:%S')
        system.search_reviews(start_time, end_time, args.task_type, args.error_code)
    elif args.command == 'add-trigger':
        system.add_scheduled_trigger(args.time, args.recurrence, args.task_type, args.day)
    elif args.command == 'list-triggers':
        system.list_scheduled_triggers()
    elif args.command == 'event-trigger':
        system.trigger_event_review(args.task_type, args.event_type, args.event_details)
    elif args.command == 'status':
        system.display_status()
    elif args.command == 'version':
        print(f"dao-review-system {get_version()}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()