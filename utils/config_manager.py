# 文件位置：.\utils\config_manager.py
"""
配置管理模块，负责读取和写入项目的配置文件。

本文件主要实现以下功能：
1. 读取配置文件（如JSON格式），获取项目的各种配置信息，如AI的API密钥、主题模式、动效是否启用等。
2. 将用户在设置界面修改后的配置信息写入配置文件，确保配置的持久化。

需要导入的库：
- `json`：用于处理JSON格式的配置文件。
- `os`：用于处理文件和目录相关操作，如检查文件是否存在。

类：
- `ConfigManager`: 配置管理类。
    - 构造函数`__init__(self)`：初始化`ConfigManager`实例，设置配置文件路径。
    - 函数`read_config(self)`：读取配置文件。
        - 尝试打开配置文件并读取内容。
        - 如果文件不存在，返回默认配置（包含默认的API密钥、主题模式、动效启用状态等）。
        - 如果读取文件时发生错误，打印错误信息并返回默认配置。
    - 函数`write_config(self, config)`：写入配置文件。
        - 尝试打开配置文件并将传入的配置字典写入文件。
        - 如果写入文件时发生错误，打印错误信息。
"""
import json
import os


class ConfigManager:
    def __init__(self):
        self.config_file_path = 'config.json'

    def read_config(self):
        if not os.path.exists(self.config_file_path):
            return {
                'openai_api_key': '',
                'theme': 'light',
                'enable_animations': True
            }
        try:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"读取配置文件时发生错误: {e}")
            return {
                'openai_api_key': '',
                'theme': 'light',
                'enable_animations': True
            }

    def write_config(self, config):
        try:
            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"写入配置文件时发生错误: {e}")
