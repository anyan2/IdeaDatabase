@echo off
rem 获取脚本所在目录
set SCRIPT_DIR=%~dp0
rem 进入脚本所在目录
cd /d %SCRIPT_DIR%

rem 激活虚拟环境（如果有）
call venv\Scripts\activate

rem 检查 PyInstaller 是否安装，如果未安装则进行安装
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller 未安装，正在安装...
    pip install pyinstaller
)

rem 编译项目
pyinstaller --onefile --distpath=dist/exe --add-data="core;core" --add-data="data;data" --add-data="ui;ui" --add-data="utils;utils" --add-data="data\ai_memory.json;data" --add-data="data\ideas.db;data" --add-data="config.json;." --hidden-import=requests  --noconsole main.py
pause
rem 退出虚拟环境（如果有）
deactivate

echo 编译完成！
pause