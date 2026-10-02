@echo off
chcp 65001 >nul
echo ========================================================
echo   Prompt Atelier - 手機與電腦同步啟動腳本
echo ========================================================
echo.
echo 正在啟動後端伺服器 (Flask) 與手機專屬安全通道...
echo.
start "Prompt Atelier Server" cmd /k "python app.py"
echo 正在生成手機專屬 HTTPS 網址，請稍候...
echo.
.\cloudflared.exe tunnel --protocol http2 --url http://127.0.0.1:5000
