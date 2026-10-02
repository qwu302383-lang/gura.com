@echo off
chcp 65001 >nul
title 移除 Gura 開機自動啟動
echo ========================================================
echo   ⚙️ 正在取消 Gura 開機自動啟動...
echo ========================================================
echo.
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
if exist "%STARTUP_DIR%\Gura_AutoStart.vbs" (
    del /f /q "%STARTUP_DIR%\Gura_AutoStart.vbs" >nul 2>&1
    echo [OK] 已成功自 Windows 開機啟動清單中移除！
) else (
    echo [提示] 尚未設定開機啟動，無需移除。
)
echo.
echo ========================================================
pause
