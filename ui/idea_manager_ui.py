from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QLineEdit, QHBoxLayout, QLabel, 
    QHeaderView, QMenu, QDialog, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QAction, QIcon, QFont, QContextMenuEvent
from core.idea_manager import IdeaManager
from typing import TYPE_CHECKING
import datetime
import json

if TYPE_CHECKING:
    from core.idea_manager import IdeaManager


class IdeaEditDialog(QDialog):
    """想法编辑对话框"""
    
    def __init__(self, idea_id, content, parent=None):
        super().__init__(parent)
        self.idea_id = idea_id
        self.setWindowTitle("编辑想法")
        self.resize(600, 400)
        
        # 设置样式
        from ui.styles import get_style_sheet
        self.setStyleSheet(get_style_sheet())
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 添加标题
        title_label = QLabel("编辑想法")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建文本编辑框
        self.text_edit = QTextEdit()
        self.text_edit.setText(content)
        layout.addWidget(self.text_edit)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("保存")
        save_button.setObjectName("primaryButton")
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def get_content(self):
        """获取编辑后的内容"""
        return self.text_edit.toPlainText().strip()


class IdeaManagerUI(QWidget):
    def __init__(self, idea_manager: 'IdeaManager'):
        super().__init__()
        self.idea_manager = idea_manager
        
        # 设置布局
        self.setup_ui()
        
        # 初始化数据
        self.update_idea_list()

    def setup_ui(self):
        """设置UI布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 创建标题和工具栏
        header_layout = QHBoxLayout()
        
        title_label = QLabel("想法管理")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # 创建搜索框
        search_layout = QHBoxLayout()
        search_label = QLabel("搜索:")
        search_layout.addWidget(search_label)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入关键词搜索...")
        self.search_edit.textChanged.connect(self.search_ideas)
        search_layout.addWidget(self.search_edit)
        
        header_layout.addLayout(search_layout)
        
        layout.addLayout(header_layout)
        
        # 创建排序按钮
        sort_layout = QHBoxLayout()
        sort_layout.addWidget(QLabel("排序方式:"))
        
        sort_time_button = QPushButton("按时间排序")
        sort_time_button.clicked.connect(self.sort_by_time)
        sort_layout.addWidget(sort_time_button)
        
        sort_keyword_button = QPushButton("按关键词排序")
        sort_keyword_button.clicked.connect(self.sort_by_keyword)
        sort_layout.addWidget(sort_keyword_button)
        
        sort_layout.addStretch()
        
        layout.addLayout(sort_layout)
        
        # 创建想法表格
        self.idea_table = QTableWidget()
        self.idea_table.setColumnCount(4)
        self.idea_table.setHorizontalHeaderLabels(["时间", "内容", "标签", "摘要"])
        self.idea_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.idea_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.idea_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.idea_table.customContextMenuRequested.connect(self.show_context_menu)
        self.idea_table.doubleClicked.connect(self.edit_idea)
        
        # 设置列宽
        self.idea_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.idea_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.idea_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.idea_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.idea_table)
        
        # 创建底部按钮
        bottom_layout = QHBoxLayout()
        
        refresh_button = QPushButton("刷新列表")
        refresh_button.clicked.connect(self.update_idea_list)
        bottom_layout.addWidget(refresh_button)
        
        analyze_button = QPushButton("触发AI分析")
        analyze_button.clicked.connect(self.trigger_ai_analysis)
        bottom_layout.addWidget(analyze_button)
        
        bottom_layout.addStretch()
        
        layout.addLayout(bottom_layout)

    def update_idea_list(self, query: str = None, sort_by: str = 'time'):
        """
        更新想法列表
        
        Args:
            query: 查询关键词
            sort_by: 排序方式
        """
        # 获取想法数据
        ideas = self.idea_manager.query_ideas(query, sort_by)
        
        # 更新表格
        self.idea_table.setRowCount(0)
        for i, idea in enumerate(ideas):
            self.idea_table.insertRow(i)
            
            # 解析时间
            timestamp = idea[0]
            try:
                dt = datetime.datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                time_str = timestamp
                
            # 解析标签
            tags_str = ""
            if idea[3]:  # 标签列
                try:
                    tags = json.loads(idea[3])
                    tags_str = ", ".join(tags)
                except Exception:
                    tags_str = str(idea[3])
            
            # 设置各列数据
            time_item = QTableWidgetItem(time_str)
            
            # 截断内容，避免过长
            content = idea[1]
            max_display_length = 100
            content_display = content if len(content) <= max_display_length else content[:max_display_length] + "..."
            content_item = QTableWidgetItem(content_display)
            
            tags_item = QTableWidgetItem(tags_str)
            summary_item = QTableWidgetItem(idea[4] or "")
            
            # 存储完整数据
            time_item.setData(Qt.ItemDataRole.UserRole, idea[2])  # 存储ID
            content_item.setData(Qt.ItemDataRole.UserRole, content)  # 存储完整内容
            
            self.idea_table.setItem(i, 0, time_item)
            self.idea_table.setItem(i, 1, content_item)
            self.idea_table.setItem(i, 2, tags_item)
            self.idea_table.setItem(i, 3, summary_item)

    def sort_by_time(self):
        """按时间排序"""
        self.update_idea_list(self.search_edit.text(), 'time')

    def sort_by_keyword(self):
        """按关键词排序"""
        self.update_idea_list(self.search_edit.text(), 'keyword')

    def search_ideas(self, query: str):
        """搜索想法"""
        self.update_idea_list(query)

    def edit_idea(self, index=None):
        """编辑想法"""
        if index is None:
            # 获取当前选中的行
            selected_items = self.idea_table.selectedItems()
            if not selected_items:
                return
            index = self.idea_table.indexFromItem(selected_items[0])
            
        # 获取想法ID和内容
        row = index.row()
        idea_id = self.idea_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        content = self.idea_table.item(row, 1).data(Qt.ItemDataRole.UserRole)
        
        # 创建编辑对话框
        dialog = IdeaEditDialog(idea_id, content, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 更新想法内容
            new_content = dialog.get_content()
            if new_content and new_content != content:
                self.idea_manager.update_idea(idea_id, new_content)
                self.update_idea_list(self.search_edit.text())

    def show_context_menu(self, position):
        """显示上下文菜单"""
        selected_items = self.idea_table.selectedItems()
        if not selected_items:
            return
            
        row = self.idea_table.indexFromItem(selected_items[0]).row()
        idea_id = self.idea_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        # 创建上下文菜单
        context_menu = QMenu(self)
        
        edit_action = QAction("编辑", self)
        edit_action.triggered.connect(lambda: self.edit_idea())
        context_menu.addAction(edit_action)
        
        view_action = QAction("查看详情", self)
        view_action.triggered.connect(lambda: self.view_idea_details(idea_id))
        context_menu.addAction(view_action)
        
        analyze_action = QAction("AI分析此想法", self)
        analyze_action.triggered.connect(lambda: self.analyze_single_idea(idea_id))
        context_menu.addAction(analyze_action)
        
        context_menu.exec(self.idea_table.mapToGlobal(position))

    def view_idea_details(self, idea_id):
        """查看想法详情"""
        idea = self.idea_manager.get_idea_details(idea_id)
        if not idea:
            QMessageBox.warning(self, "错误", "无法获取想法详情")
            return
            
        # 格式化信息
        timestamp = self.idea_manager.format_datetime(idea['timestamp'])
        tags = ", ".join(idea['tags']) if idea['tags'] else "无"
        
        # 显示详情对话框
        detail_message = (
            f"创建时间: {timestamp}\n\n"
            f"标签: {tags}\n\n"
            f"摘要: {idea['summary'] or '无'}\n\n"
            f"内容:\n{idea['content']}"
        )
        
        QMessageBox.information(self, "想法详情", detail_message)

    def analyze_single_idea(self, idea_id):
        """分析单个想法"""
        # 此处可以实现针对单个想法的AI分析
        QMessageBox.information(self, "AI分析", "正在对想法进行AI分析，请稍后查看结果。")
        
        # 触发AI处理
        self.idea_manager.trigger_ai_analysis()

    def trigger_ai_analysis(self):
        """触发AI分析所有想法"""
        # 确认对话框
        reply = QMessageBox.question(
            self, 
            "AI分析", 
            "确定要触发AI对所有想法进行分析吗？这可能需要一些时间。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 显示进度提示
            QMessageBox.information(self, "AI分析", "已开始AI分析，请稍后查看结果。")
            
            # 触发AI处理
            self.idea_manager.trigger_ai_analysis()