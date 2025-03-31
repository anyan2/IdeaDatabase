from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, 
    QCheckBox, QPushButton, QHBoxLayout,
    QComboBox, QGroupBox, QTabWidget,
    QMessageBox,QWidget
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from utils.config_manager import ConfigManager


class SettingsUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("设置")
        self.resize(500, 400)
        
        # 读取配置
        self.config_manager = ConfigManager()
        self.config = self.config_manager.read_config()
        
        # 设置样式
        from ui.styles import get_style_sheet
        self.setStyleSheet(get_style_sheet())
        
        # 设置UI
        self.setup_ui()

    def setup_ui(self):
        """设置UI布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 创建标题
        title_label = QLabel("设置")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        
        # 常规设置选项卡
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        # 主题设置
        theme_group = QGroupBox("主题设置")
        theme_layout = QVBoxLayout(theme_group)
        
        theme_label = QLabel("主题模式:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["亮色", "暗色"])
        self.theme_combo.setCurrentIndex(0 if self.config.get('theme', 'light') == 'light' else 1)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        
        # 动效设置
        animation_label = QLabel("启用动效:")
        self.animation_checkbox = QCheckBox()
        self.animation_checkbox.setChecked(self.config.get('enable_animations', True))
        animation_layout = QHBoxLayout()
        animation_layout.addWidget(animation_label)
        animation_layout.addWidget(self.animation_checkbox)
        animation_layout.addStretch()
        theme_layout.addLayout(animation_layout)
        
        general_layout.addWidget(theme_group)
        general_layout.addStretch()
        
        # AI设置选项卡
        ai_tab = QWidget()
        ai_layout = QVBoxLayout(ai_tab)
        
        # API设置
        api_group = QGroupBox("API设置")
        api_layout = QVBoxLayout(api_group)
        
        api_label = QLabel("OpenAI API密钥:")
        self.api_edit = QLineEdit()
        self.api_edit.setText(self.config.get('openai_api_key', ''))
        self.api_edit.setEchoMode(QLineEdit.EchoMode.Password)  # 密码遮掩
        self.api_edit.setPlaceholderText("输入您的OpenAI API密钥")
        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_edit)
        
        # 显示密钥复选框
        self.show_api_checkbox = QCheckBox("显示API密钥")
        self.show_api_checkbox.stateChanged.connect(self.toggle_api_visibility)
        api_layout.addWidget(self.show_api_checkbox)
        
        # AI模型设置
        model_label = QLabel("AI模型:")
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.model_combo.addItems(["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"])
        self.model_combo.setCurrentText(self.config.get('ai_model', 'gpt-3.5-turbo'))
        self.model_combo.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        api_layout.addWidget(model_label)
        api_layout.addWidget(self.model_combo)
        
        # 自动分析设置
        auto_analyze_label = QLabel("启用AI自动分析:")
        self.auto_analyze_checkbox = QCheckBox()
        self.auto_analyze_checkbox.setChecked(self.config.get('enable_auto_analyze', True))
        auto_analyze_layout = QHBoxLayout()
        auto_analyze_layout.addWidget(auto_analyze_label)
        auto_analyze_layout.addWidget(self.auto_analyze_checkbox)
        auto_analyze_layout.addStretch()
        api_layout.addLayout(auto_analyze_layout)
        
        ai_layout.addWidget(api_group)
        ai_layout.addStretch()
        
        # 添加选项卡
        tab_widget.addTab(general_tab, "常规")
        tab_widget.addTab(ai_tab, "AI设置")
        
        layout.addWidget(tab_widget)
        
        # 创建按钮
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("保存")
        self.save_button.setObjectName("primaryButton")
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)

    def toggle_api_visibility(self, state):
        """切换API密钥显示模式"""
        if state == Qt.CheckState.Checked:
            self.api_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.api_edit.setEchoMode(QLineEdit.EchoMode.Password)

    def save_settings(self):
        """保存设置"""
        try:
            # 更新配置
            self.config['openai_api_key'] = self.api_edit.text()
            self.config['theme'] = 'light' if self.theme_combo.currentIndex() == 0 else 'dark'
            self.config['enable_animations'] = self.animation_checkbox.isChecked()
            self.config['ai_model'] = self.model_combo.currentText()
            self.config['enable_auto_analyze'] = self.auto_analyze_checkbox.isChecked()
            
            # 保存到文件
            self.config_manager.write_config(self.config)
            
            # 关闭对话框
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存设置时出错: {str(e)}")