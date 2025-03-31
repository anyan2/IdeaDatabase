import sqlite3
import datetime
import json
from typing import List, Dict, Tuple, Optional
import os


class DBHandler:
    def __init__(self):
        # 确保数据目录存在
        os.makedirs('data', exist_ok=True)
        
        # 连接到SQLite数据库
        self.conn = sqlite3.connect('data/ideas.db')
        self.cursor = self.conn.cursor()
        
        # 创建想法表（如果不存在）
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            tags TEXT,
            summary TEXT
        )
        ''')
        self.conn.commit()

    def store_idea(self, idea: str) -> int:
        """
        将想法存储到数据库中
        
        Args:
            idea: 想法内容
            
        Returns:
            新插入想法的ID
        """
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute(
            "INSERT INTO ideas (content, timestamp) VALUES (?, ?)",
            (idea, timestamp)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update_idea_tags(self, idea_id: int, tags: List[str]):
        """
        更新想法的标签
        
        Args:
            idea_id: 想法ID
            tags: 标签列表
        """
        tags_json = json.dumps(tags, ensure_ascii=False)
        self.cursor.execute(
            "UPDATE ideas SET tags = ? WHERE id = ?",
            (tags_json, idea_id)
        )
        self.conn.commit()

    def update_idea_summary(self, idea_id: int, summary: str):
        """
        更新想法的摘要
        
        Args:
            idea_id: 想法ID
            summary: 摘要内容
        """
        self.cursor.execute(
            "UPDATE ideas SET summary = ? WHERE id = ?",
            (summary, idea_id)
        )
        self.conn.commit()
        
    def update_idea_content(self, idea_id: int, content: str):
        """
        更新想法的内容
        
        Args:
            idea_id: 想法ID
            content: 新的想法内容
        """
        self.cursor.execute(
            "UPDATE ideas SET content = ? WHERE id = ?",
            (content, idea_id)
        )
        self.conn.commit()

    def query_ideas(self, query: str = None, sort_by: str = 'time') -> List[Tuple]:
        """
        查询想法
        
        Args:
            query: 查询关键词，如果为None则查询所有想法
            sort_by: 排序方式，'time'按时间排序，'keyword'按关键词排序
            
        Returns:
            想法列表，每个想法为一个元组，包含(时间, 内容, ID, 标签, 摘要)
        """
        sql_query = "SELECT timestamp, content, id, tags, summary FROM ideas"
        params = []
        
        if query:
            sql_query += " WHERE content LIKE ? OR tags LIKE ?"
            params = [f'%{query}%', f'%{query}%']
        
        if sort_by == 'time':
            sql_query += " ORDER BY timestamp DESC"
        elif sort_by == 'keyword':
            # 按关键词排序时，我们将按内容的字母顺序排序
            sql_query += " ORDER BY content"
        
        self.cursor.execute(sql_query, params)
        return self.cursor.fetchall()
    
    def get_all_ideas(self) -> List[Dict]:
        """
        获取所有想法数据，用于AI处理
        
        Returns:
            想法列表，每个想法为一个字典，包含id、content、timestamp、tags和summary字段
        """
        self.cursor.execute("SELECT id, content, timestamp, tags, summary FROM ideas")
        ideas = []
        for row in self.cursor.fetchall():
            idea = {
                'id': row[0],
                'content': row[1],
                'timestamp': row[2],
                'tags': json.loads(row[3]) if row[3] else [],
                'summary': row[4]
            }
            ideas.append(idea)
        return ideas
    
    def get_idea_by_id(self, idea_id: int) -> Optional[Dict]:
        """
        根据ID获取想法
        
        Args:
            idea_id: 想法ID
            
        Returns:
            想法数据字典，如果找不到则返回None
        """
        self.cursor.execute(
            "SELECT id, content, timestamp, tags, summary FROM ideas WHERE id = ?", 
            (idea_id,)
        )
        row = self.cursor.fetchone()
        if not row:
            return None
            
        return {
            'id': row[0],
            'content': row[1],
            'timestamp': row[2],
            'tags': json.loads(row[3]) if row[3] else [],
            'summary': row[4]
        }
        
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()