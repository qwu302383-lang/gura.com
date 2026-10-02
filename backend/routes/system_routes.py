import os
import platform
import sys
import time
from flask import Blueprint, jsonify
from backend.config import DEFAULT_MODEL, PUBLIC_URL_FILE, SERVER_START_TIME
from backend.services.collab_service import get_rooms_count

system_bp = Blueprint("system", __name__)

@system_bp.get("/api/system/ping")
def ping():
    return jsonify({
        "status": "pong",
        "timestamp": time.time()
    })

@system_bp.get("/api/system/status")
def system_status():
    uptime_sec = int(time.time() - SERVER_START_TIME)
    hours, remainder = divmod(uptime_sec, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}時 {minutes}分 {seconds}秒" if hours else f"{minutes}分 {seconds}秒"

    public_url = None
    if os.path.exists(PUBLIC_URL_FILE):
        try:
            with open(PUBLIC_URL_FILE, "r", encoding="utf-8") as f:
                public_url = f.read().strip()
        except Exception:
            pass

    return jsonify({
        "status": "online",
        "backend": {
            "name": "Gura AI Backend Core",
            "runtime": f"Python {platform.python_version()}",
            "os": f"{platform.system()} {platform.release()}",
            "framework": "Flask RESTful API",
            "ai_model": DEFAULT_MODEL,
            "port": 5000,
            "uptime_seconds": uptime_sec,
            "uptime_text": uptime_str,
            "active_collab_rooms": get_rooms_count(),
            "architecture": "Separated Backend (Modular Services & Blueprints)"
        },
        "tunnel": {
            "service": "Cloudflare Quick Tunnel",
            "encryption": "TLS 1.3 / HTTP/2",
            "public_url": public_url or "未啟動或偵測中"
        },
        "frontend": {
            "name": "Gura AI Web & Mobile Client",
            "version": "v1.6 (Separated Architecture)",
            "technologies": ["HTML5", "Modern CSS3 (Responsive)", "Vanilla JavaScript (SPA)"],
            "features": [
                "語音辨識輸入 (Speech Recognition STT)",
                "多語言人聲朗讀 (Speech Synthesis TTS)",
                "手機抽屜式全螢幕對話排版",
                "多用戶專案連機輪詢器 (1.5s REST Polling)",
                "客戶端 LocalStorage 會話存儲",
                "待辦事項與手機聯動中心"
            ]
        }
    })
