@echo off
chcp 65001 >nul
title Gura 一鍵推送到 GitHub
echo ===================================================
echo     Gura 專案一鍵上傳至 GitHub (qwu302383-lang/gura.com)
echo ===================================================
echo.
echo 目標倉庫: https://github.com/qwu302383-lang/gura.com.git
echo.
echo 請選擇推送方式：
echo   [1] 直接推送 (將自動跳出瀏覽器登入授權 qwu302383-lang) [預設，按 Enter]
echo   [2] 使用 GitHub Token (PAT) 推送 (推薦：免彈窗驗證，最快速可靠)
echo   [3] 清除舊帳號快取 (hs413076-web) 後重新登入授權
echo.
set /p CHOICE="請選擇 [1/2/3] (預設 1): "

if "%CHOICE%"=="" set CHOICE=1

if "%CHOICE%"=="3" (
    echo.
    echo 正在清除舊帳號登入快取...
    cmdkey /delete:git:https://hs413076-web@github.com 2>nul
    cmdkey /delete:"GitHub for Visual Studio - https://hs413076-web@github.com/" 2>nul
    "C:\Users\ella2\AppData\Local\Programs\Git\cmd\git.exe" credential-manager reject https://github.com 2>nul
    echo 快取清除完成！接下來請在瀏覽器登入 qwu302383-lang。
    set CHOICE=1
)

if "%CHOICE%"=="2" (
    echo.
    echo 提示: 請至 https://github.com/settings/tokens 建立 Personal Access Token (Classic)
    echo (只需勾選「repo」完整權限，複製 ghp_ 開頭的字串)
    echo.
    set /p GITHUB_TOKEN="請貼上您的 GitHub Token: "
    if "%GITHUB_TOKEN%"=="" (
        echo [錯誤] 未輸入 Token。
        pause
        exit /b
    )
    set REMOTE_URL=https://qwu302383-lang:%GITHUB_TOKEN%@github.com/qwu302383-lang/gura.com.git
) else (
    set REMOTE_URL=https://github.com/qwu302383-lang/gura.com.git
)

echo.
echo [1/3] 正在配置 Git 遠端與分支...
"C:\Users\ella2\AppData\Local\Programs\Git\cmd\git.exe" remote remove origin 2>nul
"C:\Users\ella2\AppData\Local\Programs\Git\cmd\git.exe" remote add origin %REMOTE_URL%
"C:\Users\ella2\AppData\Local\Programs\Git\cmd\git.exe" branch -M main

echo [2/3] 正在推送至 GitHub main 分支...
"C:\Users\ella2\AppData\Local\Programs\Git\cmd\git.exe" push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ===================================================
    echo ⚠️ 推送失敗或需要權限驗證！
    echo ---------------------------------------------------
    echo 可能原因：
    echo 1. 您的電腦登入快取仍為其他帳號 (例如 hs413076-web)，沒有此倉庫權限。
    echo 2. 解決方法：
    echo    - 重新執行此腳本，選擇 [2] 輸入 qwu302383-lang 的 GitHub Token。
    echo    - 或重新執行此腳本，選擇 [3] 清除舊登入紀錄後重試。
    echo ===================================================
) else (
    echo.
    echo ===================================================
    echo  🎉 恭喜！專案已成功推送到 GitHub！
    echo  倉庫網址: https://github.com/qwu302383-lang/gura.com
    echo.
    echo  現在您可以前往 https://render.com 點選「New +」-^>「Web Service」
    echo  選擇此倉庫，即可一鍵上線 24/7 永久伺服器！
    echo ===================================================
)
echo.
pause
