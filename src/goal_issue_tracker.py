import os
import json
from datetime import datetime
from graphql_client import global_graphql_client

class GoalIssueTracker:
    def __init__(self):
        self.config = self.load_config()
        self.goals = []
        self.issues = []
        
        # 确保数据目录存在
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
    
    def add_goal(self, name, metric, target, actual=None, status='in_progress'):
        """添加目标"""
        # 添加目标到GraphQL
        result = global_graphql_client.add_goal(name, metric, target, actual, status)
        if result.get('ok', False):
            goal = result['goal']
            self.goals.append(goal)
            return goal
        return None
    
    def update_goal(self, goal_id, actual, status):
        """更新目标状态和实际值"""
        # 更新目标到GraphQL
        result = global_graphql_client.update_goal(goal_id, actual, status)
        if result.get('ok', False):
            # 更新本地目标列表
            for i, goal in enumerate(self.goals):
                if goal['id'] == goal_id:
                    self.goals[i] = result['goal']
                    return True
        return False
    
    def add_issue(self, description, impact, priority='medium', status='open'):
        """添加问题"""
        # 添加问题到GraphQL
        result = global_graphql_client.add_issue(description, impact, priority, status)
        if result.get('ok', False):
            issue = result['issue']
            self.issues.append(issue)
            return issue
        return None
    
    def update_issue_status(self, issue_id, status, resolution=None):
        """更新问题状态"""
        # 更新问题到GraphQL
        result = global_graphql_client.update_issue(issue_id, status, resolution)
        if result.get('ok', False):
            # 更新本地问题列表
            for i, issue in enumerate(self.issues):
                if issue['id'] == issue_id:
                    self.issues[i] = result['issue']
                    return True
        return False
    
    def get_goals(self):
        """获取所有目标"""
        # 从GraphQL获取最新目标信息
        self.goals = global_graphql_client.get_goals()
        return self.goals
    
    def get_issues(self):
        """获取所有问题"""
        # 从GraphQL获取最新问题信息
        self.issues = global_graphql_client.get_issues()
        return self.issues
    
    def get_achieved_goals(self):
        """获取已达成的目标"""
        # 从GraphQL获取最新目标信息
        self.get_goals()
        return [goal for goal in self.goals if goal['status'] == 'achieved']
    
    def get_open_issues(self):
        """获取未解决的问题"""
        # 从GraphQL获取最新问题信息
        self.get_issues()
        return [issue for issue in self.issues if issue['status'] in ['open', 'in_progress']]
    
    def save_data(self, filename=None):
        """保存数据（已迁移到GraphQL，此方法保留以保持兼容性）"""
        # 数据已通过GraphQL存储，此方法保留以保持API兼容性
        return "Data stored in GraphQL"
    
    def load_data(self, filename):
        """加载数据（已迁移到GraphQL，此方法保留以保持兼容性）"""
        # 数据已通过GraphQL存储，此方法保留以保持API兼容性
        # 从GraphQL获取最新数据
        self.goals = global_graphql_client.get_goals()
        self.issues = global_graphql_client.get_issues()
        return True
    
    def load_data_from_directory(self, directory=None):
        """加载数据（已迁移到GraphQL，此方法保留以保持兼容性）"""
        # 数据已通过GraphQL存储，此方法保留以保持API兼容性
        # 从GraphQL获取最新数据
        self.goals = global_graphql_client.get_goals()
        self.issues = global_graphql_client.get_issues()
        return True
    
    def clear_data(self):
        """清除所有数据"""
        self.goals = []
        self.issues = []
    
    def get_summary(self):
        """获取摘要"""
        # 从GraphQL获取最新数据
        self.get_goals()
        self.get_issues()
        
        total_goals = len(self.goals)
        achieved_goals = len(self.get_achieved_goals())
        total_issues = len(self.issues)
        open_issues = len(self.get_open_issues())
        
        return {
            'goals': {
                'total': total_goals,
                'achieved': achieved_goals,
                'achieved_percentage': (achieved_goals / total_goals * 100) if total_goals > 0 else 0
            },
            'issues': {
                'total': total_issues,
                'open': open_issues,
                'open_percentage': (open_issues / total_issues * 100) if total_issues > 0 else 0
            }
        }

if __name__ == "__main__":
    # 示例用法
    tracker = GoalIssueTracker()
    
    # 添加目标
    tracker.add_goal('完成任务1', '完成率', 100, 100, 'achieved')
    tracker.add_goal('完成任务2', '完成率', 100, 50, 'in_progress')
    tracker.add_goal('完成任务3', '完成率', 100, 0, 'in_progress')
    
    # 添加问题
    tracker.add_issue('任务2进度缓慢', '影响项目整体进度', 'high')
    tracker.add_issue('资源不足', '影响多个任务', 'medium')
    tracker.add_issue('技术难题', '需要额外研究', 'medium')
    
    # 更新问题状态
    tracker.update_issue_status(tracker.issues[0]['id'], 'in_progress')
    
    # 打印目标列表
    print("目标列表:")
    for goal in tracker.get_goals():
        print(f"{goal['id']}: {goal['name']} - {goal['status']} - 目标: {goal['target']} - 实际: {goal['actual']}")
    
    # 打印问题列表
    print("\n问题列表:")
    for issue in tracker.get_issues():
        print(f"{issue['id']}: {issue['description']} - {issue['status']} - 优先级: {issue['priority']}")
    
    # 打印摘要
    print("\n摘要:")
    summary = tracker.get_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    
    # 保存数据
    saved_file = tracker.save_data()
    print(f"\n数据保存到: {saved_file}")
    
    # 加载数据
    tracker.clear_data()
    print("\n清除数据后:")
    print(f"目标数量: {len(tracker.get_goals())}")
    print(f"问题数量: {len(tracker.get_issues())}")
    
    tracker.load_data_from_directory()
    print("\n加载数据后:")
    print(f"目标数量: {len(tracker.get_goals())}")
    print(f"问题数量: {len(tracker.get_issues())}")