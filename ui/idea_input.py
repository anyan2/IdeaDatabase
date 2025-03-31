from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtGui import QCloseEvent, QFont
from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QEasingCurve, Qt
from core.idea_manager import IdeaManager
from typing import TYPE_CHECKING
from ui.styles import get_style_sheet

if TYPE_CHECKING:
    from core.idea_manager import IdeaManager


class IdeaInputWindow(QDialog):
    def __init__(self, idea_manager: 'IdeaManager'):
        super().__init__()
        self.idea_manager = idea_manager
        self.setModal(True)
        self.setWindowTitle("输入想法")
        
        # 设置窗口尺寸
        self.resize(500, 400)
        
        # 设置样式
        self.setStyleSheet(get_style_sheet())
        
        # 初始化UI
        self.setup_ui()
        
        # 设置动画
        from utils.config_manager import ConfigManager
        config = ConfigManager().read_config()
        if config.get('enable_animations', True):
            self.setup_animations()

    def setup_ui(self):
        """设置UI布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 添加标题
        title_label = QLabel("记录你的想法")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 添加文本编辑框
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在这里输入你的想法...")
        layout.addWidget(self.text_edit)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("保存")
        save_button.setObjectName("primaryButton")
        save_button.clicked.connect(self.save_idea)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)

    def setup_animations(self):
        """设置动画效果"""
        # 窗口打开/关闭动画
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # 重新定义showEvent和hideEvent
        self._original_show_event = self.showEvent
        self._original_hide_event = self.hideEvent
        
        def animated_show_event(event):
            self.animation.setDirection(QPropertyAnimation.Direction.Forward)
            self.animation.start()
            self._original_show_event(event)
            
        def animated_hide_event(event):
            self.animation.setDirection(QPropertyAnimation.Direction.Backward)
            self.animation.start()
            self._original_hide_event(event)
            
        self.showEvent = animated_show_event
        self.hideEvent = animated_hide_event

    def save_idea(self):
        """保存想法"""
        idea_text = self.text_edit.toPlainText().strip()
        if idea_text:
            self.idea_manager.add_idea(idea_text)
            self.accept()
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "提示", "想法内容不能为空！")

    def closeEvent(self, event: QCloseEvent):
        """处理窗口关闭事件"""
        # 如果文本已修改且不为空，询问是否保存
        if self.text_edit.document().isModified() and self.text_edit.toPlainText().strip():
            from PyQt6.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                self, 
                "提示", 
                "有未保存的想法，是否保存？",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self.save_idea()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()