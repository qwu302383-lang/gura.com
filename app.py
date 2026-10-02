import os
import sys

# 確保專案根目錄在 Python 模組搜尋路徑中
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend import create_app

# 建立前後端分離的後端 Flask 應用實例
app = create_app()

if __name__ == "__main__":
    import socket

    def get_lan_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    lan_ip = get_lan_ip()
    print("\n" + "=" * 60)
    print(" 🚀 Gura 模組化後端伺服器 (Backend Core) 啟動中！")
    print(f" 電腦本機訪問:   http://127.0.0.1:5000")
    print(f" 手機同 Wi-Fi 訪問: http://{lan_ip}:5000")
    print("=" * 60 + "\n")

    app.run(host="0.0.0.0", port=5000, debug=True)
