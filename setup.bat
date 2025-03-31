@echo off
REM 创建虚拟环境
python -m venv venv
REM 激活虚拟环境
venv\Scripts\activate
REM 安装项目依赖
pip install -r requirements.txt
pause