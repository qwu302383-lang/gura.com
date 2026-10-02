@echo off
chcp 65001 >nul
title Gura 伺服器
cd /d "%~dp0"
python run_server.py
pause
