# 文件位置：.\main.py
"""
主程序入口，负责初始化项目环境，创建用户界面，启动后台服务。

本文件主要执行以下操作：
1. 从`utils.config_manager`导入配置管理类，初始化项目配置。
2. 从`ui.main_window`导入主窗口类，创建并显示主窗口。
3. 启动后台服务，包括注册全局快捷键和启动守护进程（若有）。

需要导入的库：
- `sys`：用于处理命令行参数和系统相关操作。
- `PyQt6.QtWidgets`：PyQt6的核心窗口部件模块，用于创建和管理UI元素。
- `utils.config_manager.ConfigManager`：配置管理类，用于读取和写入项目配置。
- `ui.main_window.MainWindow`：主窗口类，包含整个应用的主界面布局和功能逻辑。
- `core.hotkey_manager.HotkeyManager`：全局快捷键管理类，负责注册和处理快捷键事件。

函数：
- `main()`: 主函数，程序的入口点。
    - 初始化配置，创建`ConfigManager`实例并读取配置。
    - 创建`QApplication`实例，设置应用名称。
    - 创建`MainWindow`实例并显示。
    - 注册全局快捷键，创建`HotkeyManager`实例并传入主窗口对象进行快捷键注册。
    - 进入应用的事件循环，返回`sys.exit(app.exec())`的结果。
"""
import sys
from PyQt6.QtWidgets import QApplication
from utils.config_manager import ConfigManager
from ui.main_window import MainWindow
from core.hotkey_manager import HotkeyManager


def main():
    # 初始化配置
    config_manager = ConfigManager()
    config = config_manager.read_config()

    app = QApplication(sys.argv)
    app.setApplicationName('ideaSystemXS')

    main_window = MainWindow(config)
    main_window.show()

    # 注册全局快捷键
    hotkey_manager = HotkeyManager(main_window)
    hotkey_manager.register_hotkeys()

    return sys.exit(app.exec())


if __name__ == '__main__':
    main()