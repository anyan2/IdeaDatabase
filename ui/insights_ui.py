from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QScrollArea, QPushButton, QFrame, QSplitter,
    QTabWidget
)
from PyQt6.QtCore import Qt, QSize, QDate
from PyQt6.QtGui import QFont
from core.idea_manager import IdeaManager
from typing import TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from core.idea_manager import IdeaManager


class InsightCard(QFrame):
    """见解卡片组件"""
    
    def __init__(self, title, content, timestamp=None):
        super().__init__()
        self.setObjectName("insightCard")
        self.setStyleSheet("""
            #insightCard {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
                background-color: rgba(255, 255, 255, 0.7);
            }
        """)
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 添加标题
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 添加内容
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        layout.addWidget(content_label)
        
        # 添加时间戳（如果有）
        if timestamp:
            try:
                dt = datetime.datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%Y-%m-%d %H:%M")
            except:
                time_str = timestamp
                
            time_label = QLabel(f"生成于: {time_str}")
            time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.addWidget(time_label)


class ReminderCard(QFrame):
    """提醒卡片组件"""
    
    def __init__(self, content, due_date):
        super().__init__()
        self.setObjectName("reminderCard")
        self.setStyleSheet("""
            #reminderCard {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
                background-color: rgba(255, 255, 230, 0.7);
            }
        """)
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 添加内容
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        layout.addWidget(content_label)
        
        # 添加日期
        date_layout = QHBoxLayout()
        date_layout.addStretch()
        
        date_label = QLabel(f"截止日期: {due_date}")
        date_font = QFont()
        date_font.setBold(True)
        date_label.setFont(date_font)
        
        # 计算日期接近程度，设置不同颜色
        try:
            due_date_obj = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
            today = datetime.date.today()
            days_left = (due_date_obj - today).days
            
            if days_left < 0:
                date_label.setStyleSheet("color: gray;")  # 过期
            elif days_left <= 1:
                date_label.setStyleSheet("color: red;")  # 紧急
            elif days_left <= 3:
                date_label.setStyleSheet("color: orange;")  # 注意
            else:
                date_label.setStyleSheet("color: green;")  # 正常
                
        except Exception:
            pass
            
        date_layout.addWidget(date_label)
        layout.addLayout(date_layout)


class InsightsUI(QWidget):
    def __init__(self, idea_manager: 'IdeaManager'):
        super().__init__()
        self.idea_manager = idea_manager
        
        # 设置布局
        self.setup_ui()
        
        # 加载数据
        self.update_insights()

    def setup_ui(self):
        """设置UI布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 创建标题
        title_label = QLabel("见解与提醒")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 创建说明
        desc_label = QLabel("AI根据你的想法生成的见解和提醒，帮助你发现模式和机会。")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # 创建刷新按钮
        refresh_button = QPushButton("刷新数据")
        refresh_button.clicked.connect(self.update_insights)
        layout.addWidget(refresh_button)
        
        # 创建选项卡
        self.tab_widget = QTabWidget()
        
        # 见解选项卡
        insights_tab = QWidget()
        insights_layout = QVBoxLayout(insights_tab)
        
        self.insights_scroll = QScrollArea()
        self.insights_scroll.setWidgetResizable(True)
        self.insights_content = QWidget()
        self.insights_layout = QVBoxLayout(self.insights_content)
        self.insights_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.insights_scroll.setWidget(self.insights_content)
        
        insights_layout.addWidget(self.insights_scroll)
        self.tab_widget.addTab(insights_tab, "见解")
        
        # 提醒选项卡
        reminders_tab = QWidget()
        reminders_layout = QVBoxLayout(reminders_tab)
        
        self.reminders_scroll = QScrollArea()
        self.reminders_scroll.setWidgetResizable(True)
        self.reminders_content = QWidget()
        self.reminders_layout = QVBoxLayout(self.reminders_content)
        self.reminders_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.reminders_scroll.setWidget(self.reminders_content)
        
        reminders_layout.addWidget(self.reminders_scroll)
        self.tab_widget.addTab(reminders_tab, "提醒")
        
        layout.addWidget(self.tab_widget)

    def update_insights(self):
        """更新见解和提醒数据"""
        # 清空现有内容
        self._clear_layout(self.insights_layout)
        self._clear_layout(self.reminders_layout)
        
        # 获取见解
        insights = self.idea_manager.get_insights()
        if insights:
            for insight in insights:
                title = insight.get('title', '未命名见解')
                content = insight.get('content', '无内容')
                timestamp = insight.get('timestamp')
                
                card = InsightCard(title, content, timestamp)
                self.insights_layout.addWidget(card)
        else:
            no_data_label = QLabel("暂无见解数据。触发AI分析后将在这里显示见解。")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.insights_layout.addWidget(no_data_label)
            
        # 获取提醒
        reminders = self.idea_manager.get_upcoming_reminders()
        if reminders:
            # 按日期排序
            sorted_reminders = sorted(
                reminders,
                key=lambda r: r.get('due_date', '9999-12-31')
            )
            
            for reminder in sorted_reminders:
                content = reminder.get('content', '无内容')
                due_date = reminder.get('due_date', '未知日期')
                
                card = ReminderCard(content, due_date)
                self.reminders_layout.addWidget(card)
        else:
            no_data_label = QLabel("暂无提醒数据。触发AI分析后将在这里显示提醒。")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.reminders_layout.addWidget(no_data_label)

    def _clear_layout(self, layout):
        """清空布局中的所有组件"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()