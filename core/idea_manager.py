from typing import List, Dict, Tuple, Optional
import datetime


class IdeaManager:
    def __init__(self, db_handler, ai_processor):
        """
        初始化想法管理器
        
        Args:
            db_handler: 数据库处理器实例
            ai_processor: AI处理器实例
        """
        self.db_handler = db_handler
        self.ai_processor = ai_processor

    def add_idea(self, idea: str) -> int:
        """
        添加想法到数据库
        
        Args:
            idea: 想法内容
            
        Returns:
            新添加想法的ID
        """
        # 存储想法到数据库
        idea_id = self.db_handler.store_idea(idea)
        
        # 尝试使用AI处理想法（生成标签等）
        # 避免阻塞UI，仅设置一个标记，让定时任务处理
        return idea_id

    def query_ideas(self, query: str = None, sort_by: str = 'time') -> List[Tuple]:
        """
        查询想法
        
        Args:
            query: 查询关键词，如果为None则查询所有想法
            sort_by: 排序方式，'time'按时间排序，'keyword'按关键词排序
            
        Returns:
            想法列表，每个想法为一个元组，包含(时间, 内容, ID, 标签, 摘要)
        """
        return self.db_handler.query_ideas(query, sort_by)

    def update_idea(self, idea_id: int, content: str) -> bool:
        """
        更新想法内容
        
        Args:
            idea_id: 想法ID
            content: 新的想法内容
            
        Returns:
            更新是否成功
        """
        try:
            self.db_handler.update_idea_content(idea_id, content)
            return True
        except Exception as e:
            print(f"更新想法时出错: {e}")
            return False

    def get_idea_details(self, idea_id: int) -> Optional[Dict]:
        """
        获取想法详情
        
        Args:
            idea_id: 想法ID
            
        Returns:
            想法详情字典，如果找不到则返回None
        """
        return self.db_handler.get_idea_by_id(idea_id)

    def trigger_ai_analysis(self):
        """触发AI对想法的分析和总结"""
        self.ai_processor.process_ideas()

    def query_ai(self, query: str) -> str:
        """
        向AI提问关于想法的问题
        
        Args:
            query: 问题内容
            
        Returns:
            AI的回答
        """
        return self.ai_processor.query_ai(query)

    def get_upcoming_reminders(self) -> List[Dict]:
        """
        获取即将到来的提醒
        
        Returns:
            提醒列表
        """
        return self.ai_processor.get_upcoming_reminders()

    def get_insights(self) -> List[Dict]:
        """
        获取AI生成的见解
        
        Returns:
            见解列表
        """
        return self.ai_processor.get_insights()

    def format_datetime(self, timestamp: str) -> str:
        """
        格式化日期时间字符串
        
        Args:
            timestamp: ISO格式的时间戳
            
        Returns:
            格式化后的日期时间字符串
        """
        try:
            dt = datetime.datetime.fromisoformat(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            return timestamp