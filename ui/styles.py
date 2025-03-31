from PyQt6.QtWidgets import QApplication
from utils.config_manager import ConfigManager


def get_style_sheet():
    """获取应用样式表"""
    config = ConfigManager().read_config()
    theme = config.get('theme', 'light')
    
    # 通用样式
    common_style = """
    QWidget {
        font-family: Arial, sans-serif;
    }
    
    QDialog, QMainWindow {
        border-radius: 10px;
    }
    
    QPushButton {
        border-radius: 5px;
        padding: 8px 15px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }
    
    QPushButton#primaryButton {
        color: white;
        background-color: #4a86e8;
        border: none;
    }
    
    QPushButton#primaryButton:hover {
        background-color: #3a76d8;
    }
    
    QPushButton#sidebarButton {
        text-align: left;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 14px;
    }
    
    QLineEdit, QTextEdit {
        border-radius: 5px;
        padding: 8px;
        border: 1px solid rgba(0, 0, 0, 0.2);
    }
    
    QTableWidget {
        border-radius: 5px;
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    QHeaderView::section {
        background-color: transparent;
        padding: 5px;
        border: none;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        font-weight: bold;
    }
    
    QTabWidget::pane {
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 5px;
    }
    
    QTabBar::tab {
        padding: 8px 16px;
        margin-right: 2px;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
    }
    
    QTabBar::tab:selected {
        font-weight: bold;
    }
    
    QScrollArea {
        border: none;
    }
    
    QLabel#appTitle {
        font-size: 20px;
        font-weight: bold;
    }
    
    QGroupBox {
        border-radius: 5px;
        padding-top: 15px;
        font-weight: bold;
    }
    """
    
    # 亮色主题
    if theme == 'light':
        style_sheet = f"""
        {common_style}
        
        QWidget {{
            background: rgba(255, 255, 255, 0.8);
            color: #333333;
        }}
        
        #sidebar {{
            background: rgba(245, 245, 245, 0.9);
            border-right: 1px solid rgba(0, 0, 0, 0.05);
        }}
        
        QPushButton {{
            background-color: #F0F0F0;
            border: 1px solid #C0C0C0;
            color: #333333;
        }}
        
        QPushButton#sidebarButton {{
            background-color: transparent;
            border: none;
        }}
        
        QPushButton#sidebarButton:hover {{
            background-color: rgba(0, 0, 0, 0.05);
        }}
        
        QTableWidget {{
            background-color: rgba(255, 255, 255, 0.8);
            alternate-background-color: rgba(245, 245, 245, 0.8);
        }}
        
        QHeaderView::section {{
            background-color: rgba(240, 240, 240, 0.8);
            color: #333333;
        }}
        
        QTabBar::tab {{
            background-color: rgba(240, 240, 240, 0.8);
            color: #333333;
        }}
        
        QTabBar::tab:selected {{
            background-color: white;
            border-bottom: 2px solid #4a86e8;
        }}
        
        QTabWidget::pane {{
            background-color: white;
        }}
        
        QGroupBox {{
            border: 1px solid rgba(0, 0, 0, 0.1);
        }}
        
        QLineEdit, QTextEdit {{
            background-color: white;
            color: #333333;
        }}
        """
    # 暗色主题
    else:
        style_sheet = f"""
        {common_style}
        
        QWidget {{
            background: rgba(33, 33, 33, 0.8);
            color: #E0E0E0;
        }}
        
        #sidebar {{
            background: rgba(43, 43, 43, 0.9);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        QPushButton {{
            background-color: #424242;
            border: 1px solid #555555;
            color: #E0E0E0;
        }}
        
        QPushButton#sidebarButton {{
            background-color: transparent;
            border: none;
        }}
        
        QPushButton#sidebarButton:hover {{
            background-color: rgba(255, 255, 255, 0.05);
        }}
        
        QLineEdit, QTextEdit {{
            background-color: #333333;
            color: #E0E0E0;
            border: 1px solid #555555;
        }}
        
        QTableWidget {{
            background-color: rgba(40, 40, 40, 0.8);
            alternate-background-color: rgba(45, 45, 45, 0.8);
            color: #E0E0E0;
            gridline-color: #555555;
        }}
        
        QHeaderView::section {{
            background-color: rgba(50, 50, 50, 0.8);
            color: #E0E0E0;
        }}
        
        QTabBar::tab {{
            background-color: #424242;
            color: #E0E0E0;
        }}
        
        QTabBar::tab:selected {{
            background-color: #333333;
            border-bottom: 2px solid #4a86e8;
        }}
        
        QTabWidget::pane {{
            background-color: #333333;
        }}
        
        QGroupBox {{
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        """
    
    # 应用毛玻璃效果
    style_sheet += """
    QMainWindow, QDialog {
        backdrop-filter: blur(10px);
    }
    """
    
    return style_sheet