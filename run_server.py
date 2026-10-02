import os
import re
import signal
import subprocess
import sys
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(PROJECT_DIR, "server.log")
PUBLIC_URL_FILE = os.path.join(PROJECT_DIR, "public_url.txt")

# 尋找使用者桌面路徑
DESKTOP_DIRS = [
    os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "桌面"),
    os.path.join(os.environ.get("USERPROFILE", ""), "Desktop"),
    os.path.join(os.environ.get("USERPROFILE", ""), "桌面"),
]


def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    try:
        print(line)
    except Exception:
        try:
            print(line.encode("ascii", errors="replace").decode("ascii"))
        except Exception:
            pass
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def kill_existing():
    log("正在清理舊有的伺服器與穿透進程...")
    try:
        subprocess.run(
            ["taskkill", "/f", "/im", "cloudflared.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass

    try:
        ps_cmd = (
            "Get-CimInstance Win32_Process | "
            "Where-Object { ($_.CommandLine -like '*app.py*') -and ($_.ProcessId -ne "
            + str(os.getpid())
            + ") } | "
            "ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
        )
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


def update_desktop_shortcuts(public_url):
    shortcut_content = f"[InternetShortcut]\nURL={public_url}\nIconIndex=0\nIconFile=C:\\Windows\\System32\\shell32.dll\n"
    created = []
    for d in DESKTOP_DIRS:
        if os.path.exists(d):
            shortcut_path = os.path.join(d, "🌐 打開 Gura 網站.url")
            try:
                with open(shortcut_path, "w", encoding="utf-8") as f:
                    f.write(shortcut_content)
                created.append(shortcut_path)
            except Exception as e:
                log(f"無法寫入捷徑至 {shortcut_path}: {e}")

    # 同時在專案目錄內存一份
    try:
        with open(os.path.join(PROJECT_DIR, "🌐 打開 Gura 網站.url"), "w", encoding="utf-8") as f:
            f.write(shortcut_content)
    except Exception:
        pass

    log(f"已在桌面建立/更新「🌐 打開 Gura 網站」捷徑: {created}")


def main():
    log("=== Gura 獨立公開伺服器啟動中 ===")
    kill_existing()
    time.sleep(1)

    CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0

    # 1. 啟動 Flask
    python_exe = sys.executable
    app_path = os.path.join(PROJECT_DIR, "app.py")
    log(f"正在啟動 Flask 後端: {python_exe} {app_path}")

    flask_env = os.environ.copy()
    if not flask_env.get("GEMINI_MODEL"):
        flask_env["GEMINI_MODEL"] = "gemini-3.6-flash"

    flask_proc = subprocess.Popen(
        [python_exe, app_path],
        cwd=PROJECT_DIR,
        env=flask_env,
        creationflags=CREATE_NO_WINDOW,
    )

    # 2. 啟動 Cloudflare Tunnel
    cloudflared_exe = os.path.join(PROJECT_DIR, "cloudflared.exe")
    if not os.path.exists(cloudflared_exe):
        log(f"錯誤: 找不到 {cloudflared_exe}")
        flask_proc.terminate()
        return

    log("正在啟動 Cloudflare 安全公開通道...")
    cf_proc = subprocess.Popen(
        [
            cloudflared_exe,
            "tunnel",
            "--protocol",
            "http2",
            "--url",
            "http://127.0.0.1:5000",
        ],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        creationflags=CREATE_NO_WINDOW,
    )

    public_url = None
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

    # 監聽輸出抓取公開網址
    start_time = time.time()
    while time.time() - start_time < 35:
        line = cf_proc.stdout.readline()
        if not line:
            if cf_proc.poll() is not None:
                log("Cloudflare 進程意外中斷。")
                break
            time.sleep(0.2)
            continue

        match = url_pattern.search(line)
        if match:
            public_url = match.group(0)
            break

    if public_url:
        log(f"成功生成公開網址: {public_url}")
        try:
            with open(PUBLIC_URL_FILE, "w", encoding="utf-8") as f:
                f.write(public_url)
        except Exception:
            pass

        update_desktop_shortcuts(public_url)
        log("手機與電腦現在可以使用同一個網站！")
        log("您可以隨時雙擊桌面上的「🌐 打開 Gura 網站」圖示！")

        if "--open-browser" in sys.argv or "-o" in sys.argv:
            try:
                import webbrowser
                target_url = public_url or "http://127.0.0.1:5000"
                webbrowser.open(target_url)
                log(f"已在預設瀏覽器中開啟: {target_url}")
            except Exception as e:
                log(f"無法開啟瀏覽器: {e}")

        # 啟動守護執行緒持續排空管道，避免 Windows 緩衝區塞滿導致進程凍結
        def drain_pipe(pipe):
            try:
                for _ in iter(pipe.readline, ''):
                    pass
            except Exception:
                pass
            finally:
                try:
                    pipe.close()
                except Exception:
                    pass

        import threading
        drain_thread = threading.Thread(target=drain_pipe, args=(cf_proc.stdout,), daemon=True)
        drain_thread.start()
    else:
        log("警告: 未能在時間內抓取到 trycloudflare 網址，請檢查網路連線。")

    # 持續監護進程
    try:
        while True:
            time.sleep(2)
            if flask_proc.poll() is not None:
                log("Flask 伺服器已停止，正在重啟...")
                flask_proc = subprocess.Popen(
                    [python_exe, app_path],
                    cwd=PROJECT_DIR,
                    creationflags=CREATE_NO_WINDOW,
                )
            if cf_proc.poll() is not None:
                log("Cloudflare 通道已停止，正在重啟...")
                cf_proc = subprocess.Popen(
                    [
                        cloudflared_exe,
                        "tunnel",
                        "--protocol",
                        "http2",
                        "--url",
                        "http://127.0.0.1:5000",
                    ],
                    cwd=PROJECT_DIR,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=CREATE_NO_WINDOW,
                )
    except KeyboardInterrupt:
        log("接收到退出信號，正在關閉服務...")
    finally:
        flask_proc.terminate()
        cf_proc.terminate()
        log("服務已完全停止。")


if __name__ == "__main__":
    main()
