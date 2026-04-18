import os
import re
from datetime import datetime
from graphql_client import global_graphql_client

class ReviewSearch:
    def __init__(self):
        self.config = self.load_config()
        self.review_files = []
        self.review_data = []
    
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
    
    def scan_reviews(self):
        """扫描复盘记录文件"""
        review_dir = self.config['review_output_dir']
        if not os.path.exists(review_dir):
            print(f"复盘记录目录不存在: {review_dir}")
            return []
        
        # 获取所有复盘记录文件
        self.review_files = [f for f in os.listdir(review_dir) if f.startswith('review_') and f.endswith('.md')]
        self.review_files.sort(reverse=True)  # 按时间倒序排序
        
        # 解析复盘记录文件
        self.review_data = []
        for filename in self.review_files:
            file_path = os.path.join(review_dir, filename)
            data = self.parse_review_file(file_path)
            if data:
                self.review_data.append(data)
        
        return self.review_data
    
    def parse_review_file(self, file_path):
        """解析复盘记录文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取元数据
            metadata = {}
            metadata_match = re.search(r'---(.*?)---', content, re.DOTALL)
            if metadata_match:
                metadata_lines = metadata_match.group(1).strip().split('\n')
                for line in metadata_lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()
            
            # 提取基本信息
            review_id_match = re.search(r'\*\*复盘ID\*\*: (.*?)\n', content)
            datetime_match = re.search(r'\*\*日期时间\*\*: (.*?)\n', content)
            task_type_match = re.search(r'\*\*任务类型\*\*: (.*?)\n', content)
            trigger_type_match = re.search(r'\*\*触发类型\*\*: (.*?)\n', content)
            trigger_details_match = re.search(r'\*\*触发详情\*\*: (.*?)\n', content)
            
            # 提取错误信息
            errors = []
            error_table_match = re.search(r'## 错误信息\n\n(.*?)\n\n##', content, re.DOTALL)
            if error_table_match:
                error_table = error_table_match.group(1)
                error_rows = error_table.strip().split('\n')
                # 跳过表头
                for row in error_rows[2:]:  # 前两行是表头和分隔线
                    if row.strip():
                        # 提取错误代码、描述和时间
                        cells = re.split(r'\|', row)
                        if len(cells) >= 4:
                            error = {
                                'code': cells[1].strip(),
                                'message': cells[2].strip(),
                                'timestamp': cells[3].strip()
                            }
                            errors.append(error)
            
            # 提取任务完成情况
            progress_match = re.search(r'\*\*总进度\*\*: (.*?)%\n', content)
            completed_match = re.search(r'\*\*已完成项\*\*: (.*?)\n', content)
            pending_match = re.search(r'\*\*未完成项\*\*: (.*?)\n', content)
            
            # 提取目标和问题
            goals = []
            goals_table_match = re.search(r'## 已达成目标\n\n(.*?)\n\n##', content, re.DOTALL)
            if goals_table_match:
                goals_table = goals_table_match.group(1)
                goal_rows = goals_table.strip().split('\n')
                # 跳过表头
                for row in goal_rows[2:]:  # 前两行是表头和分隔线
                    if row.strip():
                        # 提取目标信息
                        cells = re.split(r'\|', row)
                        if len(cells) >= 4:
                            goal = {
                                'name': cells[1].strip(),
                                'metric': cells[2].strip(),
                                'achievement': cells[3].strip()
                            }
                            goals.append(goal)
            
            issues = []
            issues_table_match = re.search(r'## 未解决问题\n\n(.*?)\n\n##', content, re.DOTALL)
            if issues_table_match:
                issues_table = issues_table_match.group(1)
                issue_rows = issues_table.strip().split('\n')
                # 跳过表头
                for row in issue_rows[2:]:  # 前两行是表头和分隔线
                    if row.strip():
                        # 提取问题信息
                        cells = re.split(r'\|', row)
                        if len(cells) >= 5:
                            issue = {
                                'description': cells[1].strip(),
                                'status': cells[2].strip(),
                                'impact': cells[3].strip(),
                                'priority': cells[4].strip()
                            }
                            issues.append(issue)
            
            # 构建数据结构
            data = {
                'filename': os.path.basename(file_path),
                'path': file_path,
                'metadata': metadata,
                'review_id': review_id_match.group(1) if review_id_match else None,
                'datetime': datetime_match.group(1) if datetime_match else None,
                'task_type': task_type_match.group(1) if task_type_match else None,
                'trigger_type': trigger_type_match.group(1) if trigger_type_match else None,
                'trigger_details': trigger_details_match.group(1) if trigger_details_match else None,
                'errors': errors,
                'progress': float(progress_match.group(1)) if progress_match else 0.0,
                'completed_items': int(completed_match.group(1)) if completed_match else 0,
                'pending_items': int(pending_match.group(1)) if pending_match else 0,
                'goals': goals,
                'issues': issues
            }
            
            return data
        except Exception as e:
            print(f"解析文件 {file_path} 时出错: {str(e)}")
            return None
    
    def search_by_time_range(self, start_time, end_time):
        """按时间范围检索"""
        if not self.review_data:
            self.scan_reviews()
        
        results = []
        for review in self.review_data:
            if review['datetime']:
                review_time = datetime.fromisoformat(review['datetime'])
                if start_time <= review_time <= end_time:
                    results.append(review)
        
        return results
    
    def search_by_task_type(self, task_type):
        """按任务类型检索"""
        if not self.review_data:
            self.scan_reviews()
        
        results = []
        for review in self.review_data:
            if review['task_type'] == task_type:
                results.append(review)
        
        return results
    
    def search_by_error_type(self, error_code):
        """按错误类型检索"""
        if not self.review_data:
            self.scan_reviews()
        
        results = []
        for review in self.review_data:
            for error in review['errors']:
                if error['code'] == error_code:
                    results.append(review)
                    break
        
        return results
    
    def search(self, start_time=None, end_time=None, task_type=None, error_code=None):
        """综合检索"""
        if not self.review_data:
            self.scan_reviews()
        
        results = self.review_data.copy()
        
        # 按时间范围过滤
        if start_time and end_time:
            results = [r for r in results if r['datetime'] and start_time <= datetime.fromisoformat(r['datetime']) <= end_time]
        
        # 按任务类型过滤
        if task_type:
            results = [r for r in results if r['task_type'] == task_type]
        
        # 按错误类型过滤
        if error_code:
            filtered = []
            for review in results:
                for error in review['errors']:
                    if error['code'] == error_code:
                        filtered.append(review)
                        break
            results = filtered
        
        return results
    
    def display_results(self, results):
        """展示检索结果"""
        if not results:
            print("没有找到匹配的复盘记录")
            return
        
        print(f"找到 {len(results)} 条匹配的复盘记录:")
        print("-" * 100)
        
        for i, review in enumerate(results, 1):
            print(f"{i}. 文件名: {review['filename']}")
            print(f"   复盘ID: {review['review_id']}")
            print(f"   日期时间: {review['datetime']}")
            print(f"   任务类型: {review['task_type']}")
            print(f"   触发类型: {review['trigger_type']}")
            print(f"   总进度: {review['progress']}%")
            print(f"   错误数量: {len(review['errors'])}")
            print(f"   未解决问题: {len(review['issues'])}")
            print("-" * 100)

if __name__ == "__main__":
    # 示例用法
    searcher = ReviewSearch()
    
    # 扫描复盘记录
    searcher.scan_reviews()
    
    # 按时间范围检索
    print("\n1. 按时间范围检索:")
    start_time = datetime(2026, 4, 1, 0, 0, 0)
    end_time = datetime(2026, 4, 30, 23, 59, 59)
    time_results = searcher.search_by_time_range(start_time, end_time)
    searcher.display_results(time_results)
    
    # 按任务类型检索
    print("\n2. 按任务类型检索:")
    task_results = searcher.search_by_task_type('daily_review')
    searcher.display_results(task_results)
    
    # 按错误类型检索
    print("\n3. 按错误类型检索:")
    error_results = searcher.search_by_error_type('E001')
    searcher.display_results(error_results)
    
    # 综合检索
    print("\n4. 综合检索:")
    combined_results = searcher.search(
        start_time=datetime(2026, 4, 1, 0, 0, 0),
        end_time=datetime(2026, 4, 30, 23, 59, 59),
        task_type='daily_review'
    )
    searcher.display_results(combined_results)