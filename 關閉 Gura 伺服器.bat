@echo off
chcp 65001 >nul
title 關閉 Gura 伺服器
echo ========================================================
echo   🛑 正在停止 Gura 背景伺服器與穿透服務...
echo ========================================================
echo.
taskkill /f /im cloudflared.exe >nul 2>&1
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -like '*run_server.py*') -or ($_.CommandLine -like '*app.py*') } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" >nul 2>&1
echo [OK] 伺服器已全數關閉完成！
timeout /t 2 >nul
exit
