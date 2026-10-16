import os
import re
import uuid
import time
from flask import Blueprint, render_template, abort, Response, request, jsonify
from backend.config import GOOGLE_CLIENT_ID, SITES_DIR

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def home():
    return render_template("index.html", google_client_id=GOOGLE_CLIENT_ID)

@main_bp.get("/sites/<site_id>")
def view_site(site_id):
    """直接以獨立專屬網址開啟使用者生成的完整簡易網頁"""
    safe_id = re.sub(r'[^a-zA-Z0-9_-]', '', site_id)
    if not safe_id:
        abort(404)
    file_path = os.path.join(SITES_DIR, f"{safe_id}.html")
    if not os.path.exists(file_path):
        return """<!DOCTYPE html>
<html lang="zh-TW"><head><meta charset="utf-8"><title>404 網頁不存在</title>
<style>body{font-family:sans-serif;display:grid;place-items:center;height:100vh;margin:0;background:#f8fafc;color:#334155;text-align:center;}
h1{margin:0 0 8px;font-size:24px;color:#0f172a;}p{color:#64748b;}a{color:#0284c7;text-decoration:none;font-weight:600;}</style>
</head><body><div><h1>404 找不到此網頁</h1><p>該自訂網頁尚未生成或已被移除。</p><p><a href="/">← 返回 Gura 首頁</a></p></div></body></html>""", 404, {"Content-Type": "text/html; charset=utf-8"}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return Response(content, mimetype="text/html; charset=utf-8")
    except Exception as e:
        return f"無法讀取網頁：{e}", 500

@main_bp.post("/api/sites/save")
def save_site():
    """儲存網頁 HTML 並返回專屬訪問網址"""
    data = request.get_json(silent=True) or {}
    html = data.get("html", "").strip()
    title = data.get("title", "").strip() or "簡易自訂網頁"
    if not html:
        return jsonify({"error": "缺少 HTML 內容"}), 400

    short_uuid = uuid.uuid4().hex[:8]
    date_str = time.strftime("%Y%m%d")
    site_id = f"site_{date_str}_{short_uuid}"
    file_path = os.path.join(SITES_DIR, f"{site_id}.html")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

    return jsonify({
        "success": True,
        "site_id": site_id,
        "site_url": f"/sites/{site_id}",
        "title": title
    })
