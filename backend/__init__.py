import os
from flask import Flask
from backend.config import FRONTEND_STATIC_DIR, FRONTEND_TEMPLATE_DIR
from backend.routes import chat_bp, collab_bp, main_bp, system_bp

def create_app():
    """建立並配置 Flask 應用實例 (後端應用工廠)"""
    app = Flask(
        __name__,
        template_folder=FRONTEND_TEMPLATE_DIR,
        static_folder=FRONTEND_STATIC_DIR
    )
    app.json.ensure_ascii = False

    # 註冊後端模組化路由藍圖
    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(collab_bp)
    app.register_blueprint(system_bp)

    return app

__all__ = ["create_app"]
