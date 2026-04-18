import strawberry
from datetime import datetime
from typing import List, Optional, Dict, Any

# 内存存储
config_store = {
    'id': '1',
    'scheduled_triggers': [
        {
            'id': '1',
            'time': '08:00',
            'recurrence': 'daily',
            'task_type': 'daily_review'
        },
        {
            'id': '2',
            'time': '09:00',
            'recurrence': 'weekly',
            'day': 'monday',
            'task_type': 'weekly_review'
        }
    ],
    'review_output_dir': './reviews',
    'error_log_dir': './logs/errors',
    'task_data_dir': './data/tasks'
}

trigger_records = []
errors = []
exceptions = []
tasks = []
goals = []
issues = []
suggestions = []

# 工具函数
def generate_id():
    return f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

# 类型定义

@strawberry.type
class Trigger:
    id: str
    time: str
    recurrence: str
    task_type: str
    day: Optional[str] = None

@strawberry.type
class Config:
    id: str
    scheduled_triggers: List[Trigger]
    review_output_dir: str
    error_log_dir: str
    task_data_dir: str

@strawberry.type
class TriggerRecord:
    id: str
    timestamp: str
    task_type: str
    trigger_type: str
    trigger_details: str

@strawberry.type
class Error:
    id: str
    code: str
    message: str
    timestamp: str
    context: Optional[str] = None

@strawberry.type
class Exception:
    id: str
    type: str
    message: str
    timestamp: str
    stack: str
    context: Optional[str] = None

@strawberry.type
class Task:
    id: str
    name: str
    description: Optional[str] = None
    priority: str
    status: str
    created_at: str
    completed_at: Optional[str] = None
    dependencies: List[str]

@strawberry.type
class Goal:
    id: str
    name: str
    metric: str
    target: str
    actual: Optional[str] = None
    status: str
    created_at: str
    updated_at: str

@strawberry.type
class Issue:
    id: str
    description: str
    impact: str
    priority: str
    status: str
    created_at: str
    updated_at: str
    resolution: Optional[str] = None

@strawberry.type
class Suggestion:
    id: str
    type: str  # process, efficiency, quality
    content: str
    timestamp: str

# 输入类型

@strawberry.input
class TriggerInput:
    time: str
    recurrence: str
    task_type: str
    day: Optional[str] = None

@strawberry.input
class ConfigInput:
    scheduled_triggers: List[TriggerInput]
    review_output_dir: Optional[str] = None
    error_log_dir: Optional[str] = None
    task_data_dir: Optional[str] = None

@strawberry.input
class TriggerRecordInput:
    task_type: str
    trigger_type: str
    trigger_details: str

@strawberry.input
class ErrorInput:
    code: str
    message: str
    context: Optional[str] = None

@strawberry.input
class ExceptionInput:
    type: str
    message: str
    stack: str
    context: Optional[str] = None

@strawberry.input
class TaskInput:
    name: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    dependencies: Optional[List[str]] = None

@strawberry.input
class TaskUpdateInput:
    status: str

@strawberry.input
class GoalInput:
    name: str
    metric: str
    target: str
    actual: Optional[str] = None
    status: Optional[str] = "in_progress"

@strawberry.input
class GoalUpdateInput:
    actual: str
    status: str

@strawberry.input
class IssueInput:
    description: str
    impact: str
    priority: Optional[str] = "medium"
    status: Optional[str] = "open"

@strawberry.input
class IssueUpdateInput:
    status: str
    resolution: Optional[str] = None

@strawberry.input
class SuggestionInput:
    type: str
    content: str

# 查询

@strawberry.type
class Query:
    @strawberry.field
    def config(self) -> Config:
        # 转换为Config类型
        triggers = [
            Trigger(
                id=t['id'],
                time=t['time'],
                recurrence=t['recurrence'],
                task_type=t['task_type'],
                day=t.get('day')
            ) for t in config_store['scheduled_triggers']
        ]
        return Config(
            id=config_store['id'],
            scheduled_triggers=triggers,
            review_output_dir=config_store['review_output_dir'],
            error_log_dir=config_store['error_log_dir'],
            task_data_dir=config_store['task_data_dir']
        )
    
    @strawberry.field
    def trigger_records(self) -> List[TriggerRecord]:
        return [
            TriggerRecord(**record) for record in trigger_records
        ]
    
    @strawberry.field
    def errors(self) -> List[Error]:
        return [
            Error(**error) for error in errors
        ]
    
    @strawberry.field
    def exceptions(self) -> List[Exception]:
        return [
            Exception(**exception) for exception in exceptions
        ]
    
    @strawberry.field
    def tasks(self) -> List[Task]:
        return [
            Task(**task) for task in tasks
        ]
    
    @strawberry.field
    def goals(self) -> List[Goal]:
        return [
            Goal(**goal) for goal in goals
        ]
    
    @strawberry.field
    def issues(self) -> List[Issue]:
        return [
            Issue(**issue) for issue in issues
        ]
    
    @strawberry.field
    def suggestions(self) -> List[Suggestion]:
        return [
            Suggestion(**suggestion) for suggestion in suggestions
        ]

# 变更

@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_config(self, input: ConfigInput) -> Config:
        global config_store
        
        if input.scheduled_triggers:
            config_store['scheduled_triggers'] = []
            for i, trigger in enumerate(input.scheduled_triggers):
                config_store['scheduled_triggers'].append({
                    'id': str(i + 1),
                    'time': trigger.time,
                    'recurrence': trigger.recurrence,
                    'task_type': trigger.task_type,
                    'day': trigger.day
                })
        
        if input.review_output_dir:
            config_store['review_output_dir'] = input.review_output_dir
        if input.error_log_dir:
            config_store['error_log_dir'] = input.error_log_dir
        if input.task_data_dir:
            config_store['task_data_dir'] = input.task_data_dir
        
        # 转换为Config类型返回
        triggers = [
            Trigger(
                id=t['id'],
                time=t['time'],
                recurrence=t['recurrence'],
                task_type=t['task_type'],
                day=t.get('day')
            ) for t in config_store['scheduled_triggers']
        ]
        return Config(
            id=config_store['id'],
            scheduled_triggers=triggers,
            review_output_dir=config_store['review_output_dir'],
            error_log_dir=config_store['error_log_dir'],
            task_data_dir=config_store['task_data_dir']
        )
    
    @strawberry.mutation
    def add_trigger_record(self, input: TriggerRecordInput) -> TriggerRecord:
        record = {
            'id': generate_id(),
            'timestamp': datetime.now().isoformat(),
            'task_type': input.task_type,
            'trigger_type': input.trigger_type,
            'trigger_details': input.trigger_details
        }
        trigger_records.append(record)
        return TriggerRecord(**record)
    
    @strawberry.mutation
    def add_error(self, input: ErrorInput) -> Error:
        error = {
            'id': generate_id(),
            'code': input.code,
            'message': input.message,
            'timestamp': datetime.now().isoformat(),
            'context': input.context
        }
        errors.append(error)
        return Error(**error)
    
    @strawberry.mutation
    def add_exception(self, input: ExceptionInput) -> Exception:
        exception = {
            'id': generate_id(),
            'type': input.type,
            'message': input.message,
            'timestamp': datetime.now().isoformat(),
            'stack': input.stack,
            'context': input.context
        }
        exceptions.append(exception)
        return Exception(**exception)
    
    @strawberry.mutation
    def add_task(self, input: TaskInput) -> Task:
        task = {
            'id': generate_id(),
            'name': input.name,
            'description': input.description,
            'priority': input.priority or 'medium',
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'completed_at': None,
            'dependencies': input.dependencies or []
        }
        tasks.append(task)
        return Task(**task)
    
    @strawberry.mutation
    def update_task(self, task_id: str, input: TaskUpdateInput) -> Task:
        for task in tasks:
            if task['id'] == task_id:
                task['status'] = input.status
                if input.status == 'completed':
                    task['completed_at'] = datetime.now().isoformat()
                return Task(**task)
        # 如果没找到，返回一个空任务（实际应用中应该抛出异常）
        return Task(
            id='',
            name='',
            priority='',
            status='',
            created_at='',
            dependencies=[]
        )
    
    @strawberry.mutation
    def add_goal(self, input: GoalInput) -> Goal:
        goal = {
            'id': generate_id(),
            'name': input.name,
            'metric': input.metric,
            'target': input.target,
            'actual': input.actual,
            'status': input.status or 'in_progress',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        goals.append(goal)
        return Goal(**goal)
    
    @strawberry.mutation
    def update_goal(self, goal_id: str, input: GoalUpdateInput) -> Goal:
        for goal in goals:
            if goal['id'] == goal_id:
                goal['actual'] = input.actual
                goal['status'] = input.status
                goal['updated_at'] = datetime.now().isoformat()
                return Goal(**goal)
        # 如果没找到，返回一个空目标（实际应用中应该抛出异常）
        return Goal(
            id='',
            name='',
            metric='',
            target='',
            status='',
            created_at='',
            updated_at=''
        )
    
    @strawberry.mutation
    def add_issue(self, input: IssueInput) -> Issue:
        issue = {
            'id': generate_id(),
            'description': input.description,
            'impact': input.impact,
            'priority': input.priority or 'medium',
            'status': input.status or 'open',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'resolution': None
        }
        issues.append(issue)
        return Issue(**issue)
    
    @strawberry.mutation
    def update_issue(self, issue_id: str, input: IssueUpdateInput) -> Issue:
        for issue in issues:
            if issue['id'] == issue_id:
                issue['status'] = input.status
                if input.resolution:
                    issue['resolution'] = input.resolution
                issue['updated_at'] = datetime.now().isoformat()
                return Issue(**issue)
        # 如果没找到，返回一个空问题（实际应用中应该抛出异常）
        return Issue(
            id='',
            description='',
            impact='',
            priority='',
            status='',
            created_at='',
            updated_at=''
        )
    
    @strawberry.mutation
    def add_suggestion(self, input: SuggestionInput) -> Suggestion:
        suggestion = {
            'id': generate_id(),
            'type': input.type,
            'content': input.content,
            'timestamp': datetime.now().isoformat()
        }
        suggestions.append(suggestion)
        return Suggestion(**suggestion)

# 模式
schema = strawberry.Schema(query=Query, mutation=Mutation)