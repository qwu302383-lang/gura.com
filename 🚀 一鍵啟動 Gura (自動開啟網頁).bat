@echo off
chcp 65001 >nul
title Gura AI 智慧助理 - 啟動器
echo ========================================================
echo   🚀 正在啟動 Gura AI 智慧助理伺服器...
echo ========================================================
echo.
cd /d "%~dp0"

echo [1/3] 正在檢查後台進程狀態...
netstat -ano | findstr :5000 >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] 伺服器已經在背景運行中！
) else (
    echo [2/3] 正在背景啟動伺服器與穿透隧道...
    start "" "C:\Users\ella2\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe" run_server.py --open-browser
    timeout /t 3 >nul
)

echo [3/3] 正在為您開啟 Gura 網站...
if exist public_url.txt (
    for /f "usebackq tokens=*" %%A in ("public_url.txt") do start "" "%%A"
) else (
    start "" "http://127.0.0.1:5000"
)

echo.
echo ========================================================
echo   🎉 Gura 已成功啟動！您現在可以在瀏覽器盡情使用。
echo   （此視窗將於 2 秒後自動關閉，伺服器將在背景持續服務）
echo ========================================================
timeout /t 2 >nul
exit
