# ideaSystemXS

一个智能的想法管理系统，帮助你记录、整理和分析你的想法。

## 功能特点

- 全局快捷键（Ctrl+Alt+I）随时调出输入窗口，快速记录想法
- 美观的苹果风格毛玻璃UI设计，支持亮色/暗色主题
- AI智能分析，自动提取标签、生成摘要
- 智能见解和提醒，帮助发现想法中的模式和关联
- AI对话功能，直接询问有关你想法的问题
- 离线工作能力，即使AI API不可用时，也能正常使用基本功能
注意：如果需要使用本地ai 则需要修改core/ai_processor.py 中 openai.api_base = "http://127.0.0.1:1234/v1"
如果需要使用openai的接口 则把这一行注释掉。
## 系统要求

- Windows 操作系统
- Python 3.8 或更高版本
- 互联网连接（用于AI功能）

## 安装说明

1. 克隆或下载此仓库
2. 运行 `setup.bat` 安装依赖项
3. 运行 `venv.bat` 启动虚拟环境
4.输入 python main.py启动程序


## 配置说明

首次运行时，请在设置中配置您的OpenAI API密钥以启用AI功能。

## 目录结构

```
ideaSystemXS/
├── core/                 # 核心功能模块
│   ├── ai_processor.py   # AI处理器
│   ├── db_handler.py     # 数据库处理器
│   ├── hotkey_manager.py # 全局快捷键管理
│   └── idea_manager.py   # 想法管理器
├── ui/                   # 用户界面模块
│   ├── ai_console_ui.py  # AI对话界面
│   ├── idea_input.py     # 想法输入窗口
│   ├── idea_manager_ui.py # 想法管理界面
│   ├── insights_ui.py    # 见解和提醒界面
│   ├── main_window.py    # 主窗口
│   ├── settings_ui.py    # 设置界面
│   └── styles.py         # UI样式和主题
├── utils/                # 工具模块
│   └── config_manager.py # 配置管理器
├── data/                 # 数据存储目录
├── resources/            # 资源文件目录
├── main.py               # 主程序入口
├── setup.bat             # 安装脚本
├── run.bat               # 启动脚本
└── requirements.txt      # 依赖项列表
```

## 使用说明

### 记录想法

- 按下 `Ctrl+Alt+I` 或点击主界面上的"输入想法"按钮打开输入窗口
- 输入你的想法内容，点击"保存"按钮记录

### 管理想法

- 在"想法管理"页面可以查看、搜索和编辑你的所有想法
- 支持按时间或关键词排序
- 双击想法项目可以编辑内容

### AI分析

- 在"想法管理"页面点击"触发AI分析"按钮，AI将分析你的想法并生成标签、摘要
- 在"见解与提醒"页面可以查看AI根据你的想法生成的见解和提醒

### AI对话

- 在"AI对话"页面可以直接向AI提问关于你想法的问题
- AI将根据你的想法数据库提供回答

## 注意事项

- 确保API密钥正确配置以使用AI功能
- 想法数据存储在本地，请定期备份 `data` 目录
-构建目标的时候，注意exe旁边需要放config.json用于保存api配置 当然不放似乎也没事 不清楚不放的后果
## 许可证

本项目采用 MIT 许可证