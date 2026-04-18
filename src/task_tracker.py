import os
import json
from datetime import datetime
from graphql_client import global_graphql_client

class TaskTracker:
    def __init__(self):
        self.config = self.load_config()
        self.tasks = []
        
        # 确保任务数据目录存在
        os.makedirs(self.config['task_data_dir'], exist_ok=True)
    
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
    
    def add_task(self, name, description=None, priority='medium', dependencies=None):
        """添加任务"""
        # 添加任务到GraphQL
        result = global_graphql_client.add_task(name, description, priority, dependencies)
        if result.get('ok', False):
            task = result['task']
            self.tasks.append(task)
            return task
        return None
    
    def update_task_status(self, task_id, status):
        """更新任务状态"""
        # 更新任务状态到GraphQL
        result = global_graphql_client.update_task(task_id, status)
        if result.get('ok', False):
            # 更新本地任务列表
            for i, task in enumerate(self.tasks):
                if task['id'] == task_id:
                    self.tasks[i] = result['task']
                    return True
        return False
    
    def get_task(self, task_id):
        """获取任务信息"""
        # 从本地任务列表中获取
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        # 如果本地没有，从GraphQL获取
        tasks = global_graphql_client.get_tasks()
        for task in tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def get_all_tasks(self):
        """获取所有任务"""
        # 从GraphQL获取最新任务信息
        self.tasks = global_graphql_client.get_tasks()
        return self.tasks
    
    def get_tasks_by_status(self, status):
        """按状态获取任务"""
        # 从GraphQL获取最新任务信息
        self.get_all_tasks()
        return [task for task in self.tasks if task['status'] == status]
    
    def calculate_progress(self):
        """计算任务完成进度"""
        if not self.tasks:
            self.get_all_tasks()
        
        if not self.tasks:
            return 0.0
        
        completed_tasks = sum(1 for task in self.tasks if task['status'] == 'completed')
        return (completed_tasks / len(self.tasks)) * 100
    
    def get_completion_stats(self):
        """获取完成统计信息"""
        if not self.tasks:
            self.get_all_tasks()
        
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task['status'] == 'completed')
        pending_tasks = sum(1 for task in self.tasks if task['status'] == 'pending')
        in_progress_tasks = sum(1 for task in self.tasks if task['status'] == 'in_progress')
        
        return {
            'total': total_tasks,
            'completed': completed_tasks,
            'pending': pending_tasks,
            'in_progress': in_progress_tasks,
            'progress_percentage': self.calculate_progress()
        }
    
    def save_tasks(self, filename=None):
        """保存任务数据（已迁移到GraphQL，此方法保留以保持兼容性）"""
        # 任务数据已通过GraphQL存储，此方法保留以保持API兼容性
        return "Tasks stored in GraphQL"
    
    def load_tasks(self, filename):
        """加载任务数据（已迁移到GraphQL，此方法保留以保持兼容性）"""
        # 任务数据已通过GraphQL存储，此方法保留以保持API兼容性
        # 从GraphQL获取最新任务信息
        self.tasks = global_graphql_client.get_tasks()
        return True
    
    def load_tasks_from_directory(self, directory=None):
        """加载任务数据（已迁移到GraphQL，此方法保留以保持兼容性）"""
        # 任务数据已通过GraphQL存储，此方法保留以保持API兼容性
        # 从GraphQL获取最新任务信息
        self.tasks = global_graphql_client.get_tasks()
        return True
    
    def clear_tasks(self):
        """清除所有任务"""
        self.tasks = []
    
    def get_task_summary(self):
        """获取任务摘要"""
        # 从GraphQL获取最新任务信息
        self.get_all_tasks()
        
        stats = self.get_completion_stats()
        return {
            'stats': stats,
            'latest_tasks': self.tasks[-5:] if len(self.tasks) > 5 else self.tasks
        }

if __name__ == "__main__":
    # 示例用法
    tracker = TaskTracker()
    
    # 添加任务
    tracker.add_task('任务1', '测试任务1', 'high')
    tracker.add_task('任务2', '测试任务2', 'medium')
    tracker.add_task('任务3', '测试任务3', 'low')
    
    # 更新任务状态
    tracker.update_task_status(tracker.tasks[0]['id'], 'completed')
    tracker.update_task_status(tracker.tasks[1]['id'], 'in_progress')
    
    # 打印任务列表
    print("任务列表:")
    for task in tracker.get_all_tasks():
        print(f"{task['id']}: {task['name']} - {task['status']}")
    
    # 打印完成统计
    print("\n完成统计:")
    stats = tracker.get_completion_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # 保存任务数据
    saved_file = tracker.save_tasks()
    print(f"\n任务数据保存到: {saved_file}")
    
    # 加载任务数据
    tracker.clear_tasks()
    print("\n清除任务后:")
    print(f"任务数量: {len(tracker.get_all_tasks())}")
    
    tracker.load_tasks_from_directory()
    print("\n加载任务后:")
    print(f"任务数量: {len(tracker.get_all_tasks())}")
    
    # 打印任务摘要
    print("\n任务摘要:")
    summary = tracker.get_task_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))