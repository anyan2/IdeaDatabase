from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtCore import Qt


class HotkeyManager:
    def __init__(self, main_window: QWidget):
        """
        初始化快捷键管理器
        
        Args:
            main_window: 主窗口实例
        """
        self.main_window = main_window

    def register_hotkeys(self):
        """注册全局快捷键"""
        try:
            # 创建快捷键 Ctrl+Alt+I 来显示想法输入窗口
            shortcut = QShortcut(QKeySequence("Ctrl+Alt+I"), self.main_window)
            shortcut.activated.connect(self.show_idea_input_window)
            print("全局快捷键 Ctrl+Alt+I 已注册")
        except Exception as e:
            print(f"注册快捷键时出错: {e}")

    def show_idea_input_window(self):
        """显示想法输入窗口"""
        if hasattr(self.main_window, 'show_idea_input_window'):
            self.main_window.show_idea_input_window()