import os
import traceback
from datetime import datetime
import logging
from graphql_client import global_graphql_client

class ErrorCollector:
    def __init__(self):
        self.config = self.load_config()
        self.errors = []
        self.exceptions = []
        
        # 确保错误日志目录存在
        os.makedirs(self.config['error_log_dir'], exist_ok=True)
        
        # 配置日志
        logging.basicConfig(
            filename=os.path.join(self.config['error_log_dir'], f"error_{datetime.now().strftime('%Y%m%d')}.log"),
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def load_config(self):
        """加载配置"""
        config = global_graphql_client.get_config()
        if config:
            return {
                'error_log_dir': config.get('error_log_dir', './logs/errors'),
                'review_output_dir': config.get('review_output_dir', './reviews'),
                'task_data_dir': config.get('task_data_dir', './data/tasks')
            }
        return {
            'error_log_dir': './logs/errors',
            'review_output_dir': './reviews',
            'task_data_dir': './data/tasks'
        }
    
    def record_error(self, code, message, context=None):
        """记录错误信息"""
        # 记录到GraphQL
        result = global_graphql_client.add_error(code, message, context)
        
        error = {
            'id': result['error']['id'],
            'code': code,
            'message': message,
            'timestamp': result['error']['timestamp'],
            'context': context
        }
        self.errors.append(error)
        
        # 记录到日志
        logging.error(f"Error {code}: {message}")
        if context:
            logging.error(f"Context: {context}")
        
        return error
    
    def record_exception(self, ex, context=None):
        """记录异常信息"""
        exception_type = type(ex).__name__
        exception_message = str(ex)
        stack_trace = traceback.format_exc()
        
        # 记录到GraphQL
        result = global_graphql_client.add_exception(exception_type, exception_message, stack_trace, context)
        
        exception = {
            'id': result['exception']['id'],
            'type': exception_type,
            'message': exception_message,
            'timestamp': result['exception']['timestamp'],
            'stack': stack_trace,
            'context': context
        }
        self.exceptions.append(exception)
        
        # 记录到日志
        logging.error(f"Exception: {exception_type}: {exception_message}")
        logging.error(f"Stack trace: {stack_trace}")
        if context:
            logging.error(f"Context: {context}")
        
        return exception
    
    def get_errors(self):
        """获取所有错误信息"""
        # 从GraphQL获取最新错误信息
        self.errors = global_graphql_client.get_errors()
        return self.errors
    
    def get_exceptions(self):
        """获取所有异常信息"""
        # 从GraphQL获取最新异常信息
        self.exceptions = global_graphql_client.get_exceptions()
        return self.exceptions
    
    def clear_errors(self):
        """清除错误信息"""
        self.errors = []
    
    def clear_exceptions(self):
        """清除异常信息"""
        self.exceptions = []
    
    def save_errors(self, filename=None):
        """保存错误信息（已迁移到GraphQL，此方法保留以保持兼容性）"""
        # 错误信息已通过GraphQL存储，此方法保留以保持API兼容性
        return "Errors stored in GraphQL"
    
    def load_errors(self, filename):
        """加载错误信息（已迁移到GraphQL，此方法保留以保持兼容性）"""
        # 错误信息已通过GraphQL存储，此方法保留以保持API兼容性
        # 从GraphQL获取最新错误信息
        self.errors = global_graphql_client.get_errors()
        self.exceptions = global_graphql_client.get_exceptions()
        return True
    
    def get_error_summary(self):
        """获取错误摘要"""
        # 从GraphQL获取最新错误信息
        self.get_errors()
        self.get_exceptions()
        
        return {
            'error_count': len(self.errors),
            'exception_count': len(self.exceptions),
            'latest_error': self.errors[-1] if self.errors else None,
            'latest_exception': self.exceptions[-1] if self.exceptions else None
        }

# 全局错误收集器实例
global_error_collector = ErrorCollector()

# 装饰器：用于捕获函数执行过程中的异常
def error_catcher(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            global_error_collector.record_exception(e, {
                'function': func.__name__,
                'args': str(args),
                'kwargs': str(kwargs)
            })
            raise
    return wrapper

# 上下文管理器：用于捕获代码块中的异常
class error_catching:
    def __init__(self, context=None):
        self.context = context
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            global_error_collector.record_exception(exc_val, self.context)
        return False

if __name__ == "__main__":
    # 示例用法
    collector = ErrorCollector()
    
    # 记录错误
    collector.record_error('E001', '测试错误', {'test': 'value'})
    
    # 记录异常
    try:
        1 / 0
    except Exception as e:
        collector.record_exception(e, {'operation': 'division'})
    
    # 保存错误信息
    saved_file = collector.save_errors()
    print(f"Errors saved to: {saved_file}")
    
    # 打印错误摘要
    print("Error summary:", collector.get_error_summary())
    
    # 测试装饰器
    @error_catcher
    def test_function():
        raise ValueError("测试异常")
    
    try:
        test_function()
    except:
        pass
    
    # 测试上下文管理器
    with error_catching({'context': 'test block'}):
        raise RuntimeError("测试上下文异常")
    
    # 打印全局错误收集器中的错误
    print("Global errors:", global_error_collector.get_errors())
    print("Global exceptions:", global_error_collector.get_exceptions())