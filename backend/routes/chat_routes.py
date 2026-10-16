from flask import Blueprint, jsonify, request
from backend.services.gemini_service import (
    GeminiAuthenticationError,
    generate_chat_reply,
    search_web_snippets,
)

chat_bp = Blueprint("chat", __name__)

import os
import re
import uuid
import time
from backend.config import SITES_DIR

def extract_and_save_site(response_text):
    if not response_text:
        return None, None

    # 1. 完全閉合之 Markdown html 區塊
    m = re.search(r'```(?:html|xml)?\s*([\s\S]*?<!DOCTYPE[\s\S]*?)```', response_text, re.I)
    if not m:
        m = re.search(r'```(?:html|xml)?\s*(<html[\s\S]*?<\/html>)\s*```', response_text, re.I)
    if not m:
        m = re.search(r'(<!DOCTYPE\s+html[\s\S]*?<\/html>)', response_text, re.I)
    if not m:
        m = re.search(r'(<html[\s\S]*?<\/html>)', response_text, re.I)
    if not m:
        m = re.search(r'```html\s*([\s\S]*?)```', response_text, re.I)
        if m and ('<body' in m.group(1).lower() or '<style' in m.group(1).lower() or '<div' in m.group(1).lower()):
            pass
        else:
            m = None

    html = None
    if m:
        html = m.group(1).strip()
    else:
        # 2. 寬容未閉合區塊 (例如長代碼未輸出閉合標記或結尾受截斷)
        m2 = re.search(r'```html\s*([\s\S]+)', response_text, re.I)
        if m2:
            content = re.sub(r'```.*$', '', m2.group(1).strip(), flags=re.DOTALL).strip()
            if '<body' in content.lower() or '<style' in content.lower() or '<head' in content.lower() or '<!doctype' in content.lower():
                if not content.endswith('</html>'):
                    content += "\n</body>\n</html>"
                html = content
        if not html:
            m3 = re.search(r'(<!DOCTYPE\s+html[\s\S]+)', response_text, re.I) or re.search(r'(<html[\s\S]+)', response_text, re.I)
            if m3:
                content = re.sub(r'```.*$', '', m3.group(1).strip(), flags=re.DOTALL).strip()
                if not content.endswith('</html>'):
                    content += "\n</body>\n</html>"
                html = content

    if html:
        title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I)
        title = title_m.group(1).strip() if title_m and title_m.group(1).strip() else "簡易自訂網頁"
        
        short_uuid = uuid.uuid4().hex[:8]
        date_str = time.strftime("%Y%m%d")
        site_id = f"site_{date_str}_{short_uuid}"
        file_path = os.path.join(SITES_DIR, f"{site_id}.html")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
            return site_id, title
        except Exception:
            return None, None
    return None, None

@chat_bp.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    prompt = str(data.get("prompt", "")).strip()
    web_search = bool(data.get("web_search", False))
    web_builder = bool(data.get("web_builder", False))

    if not prompt:
        return jsonify({"error": "請先輸入 prompt。"}), 400

    try:
        reply_data = generate_chat_reply(prompt, web_search=web_search, web_builder=web_builder)
        site_id, site_title = extract_and_save_site(reply_data.get("response", ""))
        if site_id:
            reply_data["site_id"] = site_id
            reply_data["site_url"] = f"/sites/{site_id}"
            reply_data["site_title"] = site_title
        return jsonify(reply_data)
    except GeminiAuthenticationError as error:
        return jsonify({"error": str(error)}), 401
    except Exception as error:
        return jsonify({"error": str(error)}), 502

@chat_bp.get("/api/search")
def web_search_endpoint():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"results": []})
    try:
        results = search_web_snippets(query, max_results=5)
        return jsonify({"query": query, "results": results})
    except Exception as error:
        return jsonify({"error": str(error), "results": []}), 500
