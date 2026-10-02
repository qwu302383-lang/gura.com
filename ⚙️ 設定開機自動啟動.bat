@echo off
chcp 65001 >nul
title 設定 Gura 開機自動啟動
echo ========================================================
echo   ⚙️ 正在啟用 Gura 開機自動於背景啟動...
echo ========================================================
echo.
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
copy /y "%~dp0啟動 Gura 伺服器.vbs" "%STARTUP_DIR%\Gura_AutoStart.vbs" >nul
echo [OK] 已成功加入 Windows 開機啟動！
echo.
echo 說明：
echo 電腦每次開機或登入時，Gura 都會在背景自動運行，
echo 您不需手動開啟 VS Code，直接在手機或電腦瀏覽器即可使用！
echo.
echo ========================================================
pause
