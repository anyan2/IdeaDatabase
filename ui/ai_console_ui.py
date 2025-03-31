from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLineEdit, 
    QPushButton, QHBoxLayout, QLabel, QSplitter,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QTextCursor
from core.idea_manager import IdeaManager
from typing import TYPE_CHECKING
import threading

if TYPE_CHECKING:
    from core.idea_manager import IdeaManager


class AIConsoleUI(QWidget):
    def __init__(self, idea_manager: 'IdeaManager'):
        super().__init__()
        self.idea_manager = idea_manager
        
        # 对话历史
        self.conversation_history = []
        
        # 设置布局
        self.setup_ui()

    def setup_ui(self):
        """设置UI布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 创建标题
        title_label = QLabel("AI 对话")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 创建说明文本
        desc_label = QLabel("使用AI助手来分析和探索你的想法，提出问题或请求建议。")
        layout.addWidget(desc_label)
        
        # 创建对话区域
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setMinimumHeight(300)
        layout.addWidget(self.chat_area)
        
        # 创建输入区域
        input_layout = QHBoxLayout()
        
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("输入你的问题...")
        self.input_edit.returnPressed.connect(self.send_query)
        input_layout.addWidget(self.input_edit)
        
        send_button = QPushButton("发送")
        send_button.clicked.connect(self.send_query)
        input_layout.addWidget(send_button)
        
        layout.addLayout(input_layout)
        
        # 添加提示
        tips_label = QLabel("提示: 你可以询问关于你想法的问题，如'我最近在思考什么?'或'我有哪些关于工作的想法?'")
        tips_label.setWordWrap(True)
        layout.addWidget(tips_label)
        
        # 显示初始消息
        self.show_system_message("欢迎使用AI对话功能。输入你的问题，AI将基于你的想法数据库提供回答。")

    def show_system_message(self, message):
        """显示系统消息"""
        html = f"<div style='color: gray; margin: 5px 0;'><i>{message}</i></div>"
        self.chat_area.append(html)
        # 滚动到底部
        self.chat_area.moveCursor(QTextCursor.MoveOperation.End)

    def show_user_message(self, message):
        """显示用户消息"""
        html = f"<div style='margin: 10px 0;'><b>你:</b> {message}</div>"
        self.chat_area.append(html)
        # 滚动到底部
        self.chat_area.moveCursor(QTextCursor.MoveOperation.End)

    def show_ai_message(self, message):
        """显示AI消息"""
        html = f"<div style='background-color: rgba(230, 230, 250, 0.3); border-radius: 10px; padding: 10px; margin: 10px 0;'><b>AI:</b> {message}</div>"
        self.chat_area.append(html)
        # 滚动到底部
        self.chat_area.moveCursor(QTextCursor.MoveOperation.End)

    def show_thinking_message(self):
        """显示AI正在思考的消息"""
        self.chat_area.append("<div style='color: gray; margin: 5px 0;'><i>AI正在思考...</i></div>")
        # 滚动到底部
        self.chat_area.moveCursor(QTextCursor.MoveOperation.End)

    def send_query(self):
        """发送查询到AI"""
        query = self.input_edit.text().strip()
        if not query:
            return
            
        # 显示用户消息
        self.show_user_message(query)
        
        # 清空输入框
        self.input_edit.clear()
        
        # 显示AI正在思考
        self.show_thinking_message()
        
        # 在后台线程中处理查询，避免UI冻结
        threading.Thread(target=self.process_query, args=(query,), daemon=True).start()

    def process_query(self, query):
        """在后台处理查询"""
        try:
            # 获取AI回复
            response = self.idea_manager.query_ai(query)
            
            # 在UI线程中更新显示
            from PyQt6.QtCore import QMetaObject, Qt, Q_ARG
            QMetaObject.invokeMethod(
                self, 
                "update_ai_response", 
                Qt.ConnectionType.QueuedConnection, 
                Q_ARG(str, response)
            )
            
        except Exception as e:
            # 处理错误
            error_message = f"处理查询时出错: {str(e)}"
            QMetaObject.invokeMethod(
                self, 
                "update_ai_response", 
                Qt.ConnectionType.QueuedConnection, 
                Q_ARG(str, error_message)
            )

    def update_ai_response(self, response):
        """更新AI响应到UI"""
        # 移除"正在思考"消息
        cursor = self.chat_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()
        
        # 显示AI回复
        self.show_ai_message(response)
        
        # 保存对话历史
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })