import requests
import json

class GraphQLClient:
    def __init__(self, url='http://localhost:5000/graphql'):
        self.url = url
    
    def query(self, query, variables=None):
        """执行GraphQL查询"""
        payload = {
            'query': query,
            'variables': variables or {}
        }
        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def mutate(self, mutation, variables=None):
        """执行GraphQL变更"""
        payload = {
            'query': mutation,
            'variables': variables or {}
        }
        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        return response.json()
    
    # 配置相关操作
    def get_config(self):
        """获取配置"""
        query = '''
        query {
            config {
                id
                scheduledTriggers {
                    id
                    time
                    recurrence
                    taskType
                    day
                }
                reviewOutputDir
                errorLogDir
                taskDataDir
            }
        }
        '''
        result = self.query(query)
        config_data = result.get('data', {}).get('config')
        if config_data:
            # 转换字段名从驼峰命名到蛇形命名
            return {
                'id': config_data['id'],
                'scheduled_triggers': [
                    {
                        'id': t['id'],
                        'time': t['time'],
                        'recurrence': t['recurrence'],
                        'task_type': t['taskType'],
                        'day': t.get('day')
                    } for t in config_data['scheduledTriggers']
                ],
                'review_output_dir': config_data['reviewOutputDir'],
                'error_log_dir': config_data['errorLogDir'],
                'task_data_dir': config_data['taskDataDir']
            }
        return None
    
    def update_config(self, input):
        """更新配置"""
        mutation = '''
        mutation UpdateConfig($input: ConfigInput!) {
            updateConfig(input: $input) {
                id
                scheduledTriggers {
                    id
                    time
                    recurrence
                    taskType
                    day
                }
                reviewOutputDir
                errorLogDir
                taskDataDir
            }
        }
        '''
        # 转换字段名从蛇形命名到驼峰命名
        variables = {
            'input': {
                'scheduledTriggers': [
                    {
                        'time': t['time'],
                        'recurrence': t['recurrence'],
                        'taskType': t['task_type'],
                        'day': t.get('day')
                    } for t in input['scheduled_triggers']
                ]
            }
        }
        if 'review_output_dir' in input:
            variables['input']['reviewOutputDir'] = input['review_output_dir']
        if 'error_log_dir' in input:
            variables['input']['errorLogDir'] = input['error_log_dir']
        if 'task_data_dir' in input:
            variables['input']['taskDataDir'] = input['task_data_dir']
        
        result = self.mutate(mutation, variables)
        config_data = result.get('data', {}).get('updateConfig')
        if config_data:
            # 转换字段名从驼峰命名到蛇形命名
            return {
                'ok': True,
                'config': {
                    'id': config_data['id'],
                    'scheduled_triggers': [
                        {
                            'id': t['id'],
                            'time': t['time'],
                            'recurrence': t['recurrence'],
                            'task_type': t['taskType'],
                            'day': t.get('day')
                        } for t in config_data['scheduledTriggers']
                    ],
                    'review_output_dir': config_data['reviewOutputDir'],
                    'error_log_dir': config_data['errorLogDir'],
                    'task_data_dir': config_data['taskDataDir']
                }
            }
        return {'ok': False, 'config': None}
    
    # 触发记录相关操作
    def add_trigger_record(self, task_type, trigger_type, trigger_details):
        """添加触发记录"""
        mutation = '''
        mutation AddTriggerRecord($input: TriggerRecordInput!) {
            addTriggerRecord(input: $input) {
                id
                timestamp
                taskType
                triggerType
                triggerDetails
            }
        }
        '''
        variables = {
            'input': {
                'taskType': task_type,
                'triggerType': trigger_type,
                'triggerDetails': trigger_details
            }
        }
        result = self.mutate(mutation, variables)
        record_data = result.get('data', {}).get('addTriggerRecord')
        if record_data:
            return {
                'ok': True,
                'trigger_record': {
                    'id': record_data['id'],
                    'timestamp': record_data['timestamp'],
                    'task_type': record_data['taskType'],
                    'trigger_type': record_data['triggerType'],
                    'trigger_details': record_data['triggerDetails']
                }
            }
        return {'ok': False, 'trigger_record': None}
    
    def get_trigger_records(self):
        """获取触发记录"""
        query = '''
        query {
            triggerRecords {
                id
                timestamp
                taskType
                triggerType
                triggerDetails
            }
        }
        '''
        result = self.query(query)
        records_data = result.get('data', {}).get('triggerRecords')
        if records_data:
            return [
                {
                    'id': r['id'],
                    'timestamp': r['timestamp'],
                    'task_type': r['taskType'],
                    'trigger_type': r['triggerType'],
                    'trigger_details': r['triggerDetails']
                } for r in records_data
            ]
        return []
    
    # 错误相关操作
    def add_error(self, code, message, context=None):
        """添加错误"""
        mutation = '''
        mutation AddError($input: ErrorInput!) {
            addError(input: $input) {
                id
                code
                message
                timestamp
                context
            }
        }
        '''
        variables = {
            'input': {
                'code': code,
                'message': message,
                'context': context
            }
        }
        result = self.mutate(mutation, variables)
        error_data = result.get('data', {}).get('addError')
        if error_data:
            return {
                'ok': True,
                'error': {
                    'id': error_data['id'],
                    'code': error_data['code'],
                    'message': error_data['message'],
                    'timestamp': error_data['timestamp'],
                    'context': error_data.get('context')
                }
            }
        return {'ok': False, 'error': None}
    
    def add_exception(self, exception_type, message, stack, context=None):
        """添加异常"""
        mutation = '''
        mutation AddException($input: ExceptionInput!) {
            addException(input: $input) {
                id
                type
                message
                timestamp
                stack
                context
            }
        }
        '''
        variables = {
            'input': {
                'type': exception_type,
                'message': message,
                'stack': stack,
                'context': context
            }
        }
        result = self.mutate(mutation, variables)
        exception_data = result.get('data', {}).get('addException')
        if exception_data:
            return {
                'ok': True,
                'exception': {
                    'id': exception_data['id'],
                    'type': exception_data['type'],
                    'message': exception_data['message'],
                    'timestamp': exception_data['timestamp'],
                    'stack': exception_data['stack'],
                    'context': exception_data.get('context')
                }
            }
        return {'ok': False, 'exception': None}
    
    def get_errors(self):
        """获取错误"""
        query = '''
        query {
            errors {
                id
                code
                message
                timestamp
                context
            }
        }
        '''
        result = self.query(query)
        errors_data = result.get('data', {}).get('errors')
        if errors_data:
            return [
                {
                    'id': e['id'],
                    'code': e['code'],
                    'message': e['message'],
                    'timestamp': e['timestamp'],
                    'context': e.get('context')
                } for e in errors_data
            ]
        return []
    
    def get_exceptions(self):
        """获取异常"""
        query = '''
        query {
            exceptions {
                id
                type
                message
                timestamp
                stack
                context
            }
        }
        '''
        result = self.query(query)
        exceptions_data = result.get('data', {}).get('exceptions')
        if exceptions_data:
            return [
                {
                    'id': e['id'],
                    'type': e['type'],
                    'message': e['message'],
                    'timestamp': e['timestamp'],
                    'stack': e['stack'],
                    'context': e.get('context')
                } for e in exceptions_data
            ]
        return []
    
    # 任务相关操作
    def add_task(self, name, description=None, priority='medium', dependencies=None):
        """添加任务"""
        mutation = '''
        mutation AddTask($input: TaskInput!) {
            addTask(input: $input) {
                id
                name
                description
                priority
                status
                createdAt
                completedAt
                dependencies
            }
        }
        '''
        variables = {
            'input': {
                'name': name,
                'description': description,
                'priority': priority,
                'dependencies': dependencies or []
            }
        }
        result = self.mutate(mutation, variables)
        task_data = result.get('data', {}).get('addTask')
        if task_data:
            return {
                'ok': True,
                'task': {
                    'id': task_data['id'],
                    'name': task_data['name'],
                    'description': task_data.get('description'),
                    'priority': task_data['priority'],
                    'status': task_data['status'],
                    'created_at': task_data['createdAt'],
                    'completed_at': task_data.get('completedAt'),
                    'dependencies': task_data['dependencies']
                }
            }
        return {'ok': False, 'task': None}
    
    def update_task(self, task_id, status):
        """更新任务状态"""
        mutation = '''
        mutation UpdateTask($taskId: String!, $input: TaskUpdateInput!) {
            updateTask(taskId: $taskId, input: $input) {
                id
                name
                description
                priority
                status
                createdAt
                completedAt
                dependencies
            }
        }
        '''
        variables = {
            'taskId': task_id,
            'input': {
                'status': status
            }
        }
        result = self.mutate(mutation, variables)
        task_data = result.get('data', {}).get('updateTask')
        if task_data:
            return {
                'ok': True,
                'task': {
                    'id': task_data['id'],
                    'name': task_data['name'],
                    'description': task_data.get('description'),
                    'priority': task_data['priority'],
                    'status': task_data['status'],
                    'created_at': task_data['createdAt'],
                    'completed_at': task_data.get('completedAt'),
                    'dependencies': task_data['dependencies']
                }
            }
        return {'ok': False, 'task': None}
    
    def get_tasks(self):
        """获取任务"""
        query = '''
        query {
            tasks {
                id
                name
                description
                priority
                status
                createdAt
                completedAt
                dependencies
            }
        }
        '''
        result = self.query(query)
        tasks_data = result.get('data', {}).get('tasks')
        if tasks_data:
            return [
                {
                    'id': t['id'],
                    'name': t['name'],
                    'description': t.get('description'),
                    'priority': t['priority'],
                    'status': t['status'],
                    'created_at': t['createdAt'],
                    'completed_at': t.get('completedAt'),
                    'dependencies': t['dependencies']
                } for t in tasks_data
            ]
        return []
    
    # 目标相关操作
    def add_goal(self, name, metric, target, actual=None, status='in_progress'):
        """添加目标"""
        mutation = '''
        mutation AddGoal($input: GoalInput!) {
            addGoal(input: $input) {
                id
                name
                metric
                target
                actual
                status
                createdAt
                updatedAt
            }
        }
        '''
        variables = {
            'input': {
                'name': name,
                'metric': metric,
                'target': target,
                'actual': actual,
                'status': status
            }
        }
        result = self.mutate(mutation, variables)
        goal_data = result.get('data', {}).get('addGoal')
        if goal_data:
            return {
                'ok': True,
                'goal': {
                    'id': goal_data['id'],
                    'name': goal_data['name'],
                    'metric': goal_data['metric'],
                    'target': goal_data['target'],
                    'actual': goal_data.get('actual'),
                    'status': goal_data['status'],
                    'created_at': goal_data['createdAt'],
                    'updated_at': goal_data['updatedAt']
                }
            }
        return {'ok': False, 'goal': None}
    
    def update_goal(self, goal_id, actual, status):
        """更新目标"""
        mutation = '''
        mutation UpdateGoal($goalId: String!, $input: GoalUpdateInput!) {
            updateGoal(goalId: $goalId, input: $input) {
                id
                name
                metric
                target
                actual
                status
                createdAt
                updatedAt
            }
        }
        '''
        variables = {
            'goalId': goal_id,
            'input': {
                'actual': actual,
                'status': status
            }
        }
        result = self.mutate(mutation, variables)
        goal_data = result.get('data', {}).get('updateGoal')
        if goal_data:
            return {
                'ok': True,
                'goal': {
                    'id': goal_data['id'],
                    'name': goal_data['name'],
                    'metric': goal_data['metric'],
                    'target': goal_data['target'],
                    'actual': goal_data['actual'],
                    'status': goal_data['status'],
                    'created_at': goal_data['createdAt'],
                    'updated_at': goal_data['updatedAt']
                }
            }
        return {'ok': False, 'goal': None}
    
    def get_goals(self):
        """获取目标"""
        query = '''
        query {
            goals {
                id
                name
                metric
                target
                actual
                status
                createdAt
                updatedAt
            }
        }
        '''
        result = self.query(query)
        goals_data = result.get('data', {}).get('goals')
        if goals_data:
            return [
                {
                    'id': g['id'],
                    'name': g['name'],
                    'metric': g['metric'],
                    'target': g['target'],
                    'actual': g.get('actual'),
                    'status': g['status'],
                    'created_at': g['createdAt'],
                    'updated_at': g['updatedAt']
                } for g in goals_data
            ]
        return []
    
    # 问题相关操作
    def add_issue(self, description, impact, priority='medium', status='open'):
        """添加问题"""
        mutation = '''
        mutation AddIssue($input: IssueInput!) {
            addIssue(input: $input) {
                id
                description
                impact
                priority
                status
                createdAt
                updatedAt
                resolution
            }
        }
        '''
        variables = {
            'input': {
                'description': description,
                'impact': impact,
                'priority': priority,
                'status': status
            }
        }
        result = self.mutate(mutation, variables)
        issue_data = result.get('data', {}).get('addIssue')
        if issue_data:
            return {
                'ok': True,
                'issue': {
                    'id': issue_data['id'],
                    'description': issue_data['description'],
                    'impact': issue_data['impact'],
                    'priority': issue_data['priority'],
                    'status': issue_data['status'],
                    'created_at': issue_data['createdAt'],
                    'updated_at': issue_data['updatedAt'],
                    'resolution': issue_data.get('resolution')
                }
            }
        return {'ok': False, 'issue': None}
    
    def update_issue(self, issue_id, status, resolution=None):
        """更新问题"""
        mutation = '''
        mutation UpdateIssue($issueId: String!, $input: IssueUpdateInput!) {
            updateIssue(issueId: $issueId, input: $input) {
                id
                description
                impact
                priority
                status
                createdAt
                updatedAt
                resolution
            }
        }
        '''
        variables = {
            'issueId': issue_id,
            'input': {
                'status': status,
                'resolution': resolution
            }
        }
        result = self.mutate(mutation, variables)
        issue_data = result.get('data', {}).get('updateIssue')
        if issue_data:
            return {
                'ok': True,
                'issue': {
                    'id': issue_data['id'],
                    'description': issue_data['description'],
                    'impact': issue_data['impact'],
                    'priority': issue_data['priority'],
                    'status': issue_data['status'],
                    'created_at': issue_data['createdAt'],
                    'updated_at': issue_data['updatedAt'],
                    'resolution': issue_data.get('resolution')
                }
            }
        return {'ok': False, 'issue': None}
    
    def get_issues(self):
        """获取问题"""
        query = '''
        query {
            issues {
                id
                description
                impact
                priority
                status
                createdAt
                updatedAt
                resolution
            }
        }
        '''
        result = self.query(query)
        issues_data = result.get('data', {}).get('issues')
        if issues_data:
            return [
                {
                    'id': i['id'],
                    'description': i['description'],
                    'impact': i['impact'],
                    'priority': i['priority'],
                    'status': i['status'],
                    'created_at': i['createdAt'],
                    'updated_at': i['updatedAt'],
                    'resolution': i.get('resolution')
                } for i in issues_data
            ]
        return []
    
    # 建议相关操作
    def add_suggestion(self, suggestion_type, content):
        """添加建议"""
        mutation = '''
        mutation AddSuggestion($input: SuggestionInput!) {
            addSuggestion(input: $input) {
                id
                type
                content
                timestamp
            }
        }
        '''
        variables = {
            'input': {
                'type': suggestion_type,
                'content': content
            }
        }
        result = self.mutate(mutation, variables)
        suggestion_data = result.get('data', {}).get('addSuggestion')
        if suggestion_data:
            return {
                'ok': True,
                'suggestion': {
                    'id': suggestion_data['id'],
                    'type': suggestion_data['type'],
                    'content': suggestion_data['content'],
                    'timestamp': suggestion_data['timestamp']
                }
            }
        return {'ok': False, 'suggestion': None}
    
    def get_suggestions(self):
        """获取建议"""
        query = '''
        query {
            suggestions {
                id
                type
                content
                timestamp
            }
        }
        '''
        result = self.query(query)
        suggestions_data = result.get('data', {}).get('suggestions')
        if suggestions_data:
            return [
                {
                    'id': s['id'],
                    'type': s['type'],
                    'content': s['content'],
                    'timestamp': s['timestamp']
                } for s in suggestions_data
            ]
        return []

# 全局客户端实例
global_graphql_client = GraphQLClient()