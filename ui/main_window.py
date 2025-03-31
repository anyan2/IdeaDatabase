from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, 
    QLabel, QStackedWidget, QMessageBox, QSplitter
)
from PyQt6.QtGui import QIcon, QCloseEvent, QFont
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
import os

from ui.idea_input import IdeaInputWindow
from ui.idea_manager_ui import IdeaManagerUI
from ui.settings_ui import SettingsUI
from ui.ai_console_ui import AIConsoleUI
from ui.insights_ui import InsightsUI
from ui.styles import get_style_sheet
from core.db_handler import DBHandler
from core.idea_manager import IdeaManager
from core.ai_processor import AIProcessor


class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle('ideaSystemXS')
        
        # 尝试加载图标
        icon_path = 'resources/icon.ico'
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setGeometry(100, 100, 900, 600)
        
        # 设置样式表
        self.setStyleSheet(get_style_sheet())
        
        # 初始化核心组件
        self.db_handler = DBHandler()
        self.ai_processor = AIProcessor(
            self.db_handler, 
            self.config.get('openai_api_key', '')
        )
        self.idea_manager = IdeaManager(self.db_handler, self.ai_processor)
        
        # 启动AI定时任务，如果API键已设置
        if self.config.get('openai_api_key'):
            self.ai_processor.schedule_ai_task(3600)  # 每小时处理一次
        
        # 创建主界面
        self.setup_ui()

    def setup_ui(self):
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建侧边栏
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar")
        sidebar_widget.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)
        
        # 添加标题
        title_label = QLabel("ideaSystemXS")
        title_label.setObjectName("appTitle")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title_label)
        
        sidebar_layout.addSpacing(20)
        
        # 添加侧边栏按钮
        self.idea_input_button = QPushButton('✏️ 输入想法')
        self.idea_input_button.setObjectName("sidebarButton")
        self.idea_input_button.clicked.connect(self.show_idea_input_window)
        sidebar_layout.addWidget(self.idea_input_button)
        
        self.idea_manager_button = QPushButton('📚 想法管理')
        self.idea_manager_button.setObjectName("sidebarButton")
        self.idea_manager_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))
        sidebar_layout.addWidget(self.idea_manager_button)
        
        self.ai_console_button = QPushButton('🤖 AI对话')
        self.ai_console_button.setObjectName("sidebarButton")
        self.ai_console_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))
        sidebar_layout.addWidget(self.ai_console_button)
        
        self.insights_button = QPushButton('💡 见解与提醒')
        self.insights_button.setObjectName("sidebarButton")
        self.insights_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(2))
        sidebar_layout.addWidget(self.insights_button)
        
        sidebar_layout.addStretch()
        
        self.settings_button = QPushButton('⚙️ 设置')
        self.settings_button.setObjectName("sidebarButton")
        self.settings_button.clicked.connect(self.show_settings_window)
        sidebar_layout.addWidget(self.settings_button)
        
        # 添加侧边栏到主布局
        main_layout.addWidget(sidebar_widget)
        
        # 创建内容区
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建堆叠小部件以切换不同页面
        self.stack_widget = QStackedWidget()
        
        # 创建想法管理页面
        self.idea_manager_ui = IdeaManagerUI(self.idea_manager)
        self.stack_widget.addWidget(self.idea_manager_ui)
        
        # 创建AI控制台页面
        self.ai_console_ui = AIConsoleUI(self.idea_manager)
        self.stack_widget.addWidget(self.ai_console_ui)
        
        # 创建见解页面
        self.insights_ui = InsightsUI(self.idea_manager)
        self.stack_widget.addWidget(self.insights_ui)
        
        content_layout.addWidget(self.stack_widget)
        
        # 添加内容区到主布局
        main_layout.addWidget(content_widget)
        
        # 添加动画效果
        if self.config.get('enable_animations', True):
            self.setup_animations()

    def setup_animations(self):
        """设置UI动画效果"""
        # 侧边栏按钮悬停效果
        for button in self.findChildren(QPushButton, "sidebarButton"):
            button.enterEvent = lambda e, b=button: self.button_hover_animation(b, True)
            button.leaveEvent = lambda e, b=button: self.button_hover_animation(b, False)

    def button_hover_animation(self, button, hover_in):
        """按钮悬停动画效果"""
        animation = QPropertyAnimation(button, b"minimumHeight")
        animation.setDuration(150)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        if hover_in:
            animation.setStartValue(button.height())
            animation.setEndValue(button.height() + 5)
        else:
            animation.setStartValue(button.height())
            animation.setEndValue(button.height() - 5)
            
        animation.start()

    def show_idea_input_window(self):
        """显示想法输入窗口"""
        self.idea_input_window = IdeaInputWindow(self.idea_manager)
        self.idea_input_window.accepted.connect(self.idea_manager_ui.update_idea_list)
        self.idea_input_window.exec()

    def show_settings_window(self):
        """显示设置窗口"""
        self.settings_ui = SettingsUI()
        if self.settings_ui.exec() == SettingsUI.DialogCode.Accepted:
            # 重新读取配置
            from utils.config_manager import ConfigManager
            self.config = ConfigManager().read_config()
            
            # 更新界面样式
            self.setStyleSheet(get_style_sheet())
            
            # 更新AI处理器配置
            self.ai_processor.update_config(
            #self.ai_processor.openai_api_key = self.config.get('openai_api_key', '')
            api_key=self.config.get('openai_api_key', ''),
            model=self.config.get('ai_model','gpt-3.5-turbo')
            )
            # 如果设置了API密钥，启动AI任务
            if self.config.get('openai_api_key'):
                self.ai_processor.schedule_ai_task(3600)
                
            # 提示用户设置已保存
            QMessageBox.information(self, "设置", "设置已保存")

    def closeEvent(self, event: QCloseEvent):
        """处理窗口关闭事件"""
        # 关闭数据库连接
        if hasattr(self, 'db_handler'):
            self.db_handler.close()
        
        # 接受关闭事件
        event.accept()