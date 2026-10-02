import os
import time

# 專案根目錄與資料目錄
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
ROOMS_DIR = os.path.join(DATA_DIR, "collab_rooms")
os.makedirs(ROOMS_DIR, exist_ok=True)

PUBLIC_URL_FILE = os.path.join(PROJECT_ROOT, "public_url.txt")

# 前端模板與靜態資源目錄 (優先讀取 frontend/，相容根目錄 templates/static)
FRONTEND_TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "frontend", "templates")
if not os.path.exists(FRONTEND_TEMPLATE_DIR):
    FRONTEND_TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "templates")

FRONTEND_STATIC_DIR = os.path.join(PROJECT_ROOT, "frontend", "static")
if not os.path.exists(FRONTEND_STATIC_DIR):
    FRONTEND_STATIC_DIR = os.path.join(PROJECT_ROOT, "static")

# Google 與 Gemini 模型設定
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash").strip()

SERVER_START_TIME = time.time()
