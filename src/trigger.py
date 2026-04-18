import schedule
import time
import threading
import os
from datetime import datetime
from graphql_client import global_graphql_client

class ReviewTrigger:
    def __init__(self):
        self.config = self.load_config()
        self.running = False
        self.thread = None
    
    def load_config(self):
        """加载配置"""
        config = global_graphql_client.get_config()
        if config:
            # 转换配置格式
            return {
                'scheduled_triggers': [
                    {
                        'time': t['time'],
                        'recurrence': t['recurrence'],
                        'task_type': t['task_type'],
                        'day': t.get('day')
                    } for t in config.get('scheduled_triggers', [])
                ],
                'review_output_dir': config.get('review_output_dir', './reviews'),
                'error_log_dir': config.get('error_log_dir', './logs/errors'),
                'task_data_dir': config.get('task_data_dir', './data/tasks')
            }
        return {
            'scheduled_triggers': [
                {'time': '08:00', 'recurrence': 'daily', 'task_type': 'daily_review'},
                {'time': '09:00', 'recurrence': 'weekly', 'day': 'monday', 'task_type': 'weekly_review'}
            ],
            'review_output_dir': './reviews',
            'error_log_dir': './logs/errors',
            'task_data_dir': './data/tasks'
        }
    
    def save_config(self):
        """保存配置"""
        # 转换为GraphQL输入格式
        input_config = {
            'scheduled_triggers': [
                {
                    'time': t['time'],
                    'recurrence': t['recurrence'],
                    'task_type': t['task_type'],
                    'day': t.get('day')
                } for t in self.config['scheduled_triggers']
            ],
            'review_output_dir': self.config['review_output_dir'],
            'error_log_dir': self.config.get('error_log_dir', './logs/errors'),
            'task_data_dir': self.config.get('task_data_dir', './data/tasks')
        }
        result = global_graphql_client.update_config(input_config)
        return result.get('ok', False)
    
    def add_scheduled_trigger(self, time_str, recurrence, task_type, day=None):
        """添加定期触发规则"""
        trigger = {
            'time': time_str,
            'recurrence': recurrence,
            'task_type': task_type
        }
        if recurrence == 'weekly' and day:
            trigger['day'] = day
        self.config['scheduled_triggers'].append(trigger)
        self.save_config()
        self.setup_scheduled_triggers()
    
    def remove_scheduled_trigger(self, index):
        """移除定期触发规则"""
        if 0 <= index < len(self.config['scheduled_triggers']):
            self.config['scheduled_triggers'].pop(index)
            self.save_config()
            self.setup_scheduled_triggers()
    
    def setup_scheduled_triggers(self):
        """设置定期触发规则"""
        # 清除所有现有任务
        schedule.clear()
        
        # 添加新任务
        for trigger in self.config['scheduled_triggers']:
            time_str = trigger['time']
            task_type = trigger['task_type']
            
            if trigger['recurrence'] == 'daily':
                schedule.every().day.at(time_str).do(self.trigger_review, task_type=task_type, trigger_type='scheduled', trigger_details=f'Daily at {time_str}')
            elif trigger['recurrence'] == 'weekly' and 'day' in trigger:
                day = trigger['day']
                getattr(schedule.every(), day).at(time_str).do(self.trigger_review, task_type=task_type, trigger_type='scheduled', trigger_details=f'Weekly on {day} at {time_str}')
    
    def trigger_review(self, task_type, trigger_type, trigger_details):
        """触发复盘"""
        print(f"\nTriggering review: {task_type} - {trigger_type} - {trigger_details}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        # 这里将调用复盘处理逻辑
        # 暂时只打印信息
        
        # 确保输出目录存在
        os.makedirs(self.config['review_output_dir'], exist_ok=True)
        
        # 保存触发记录到GraphQL
        result = global_graphql_client.add_trigger_record(task_type, trigger_type, trigger_details)
        if result.get('ok', False):
            print(f"Trigger record saved to GraphQL: {result['trigger_record']['id']}")
        else:
            print("Failed to save trigger record to GraphQL")
    
    def trigger_event_based_review(self, task_type, event_type, event_details):
        """触发基于事件的复盘"""
        self.trigger_review(
            task_type=task_type,
            trigger_type='event-based',
            trigger_details=f"{event_type}: {event_details}"
        )
    
    def start(self):
        """启动触发服务"""
        self.running = True
        self.setup_scheduled_triggers()
        
        def run_scheduler():
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        
        self.thread = threading.Thread(target=run_scheduler)
        self.thread.daemon = True
        self.thread.start()
        print("Review trigger service started")
    
    def stop(self):
        """停止触发服务"""
        self.running = False
        if self.thread:
            self.thread.join()
        print("Review trigger service stopped")

if __name__ == "__main__":
    # 示例用法
    trigger = ReviewTrigger()
    
    # 启动服务
    trigger.start()
    
    # 添加一个额外的定期触发
    trigger.add_scheduled_trigger('12:00', 'daily', 'midday_review')
    
    # 触发一个基于事件的复盘
    trigger.trigger_event_based_review('task_completion', 'task_finished', 'Task XYZ completed')
    
    # 运行一段时间
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        trigger.stop()
        print("Exited")