from flask import Blueprint, jsonify, request
from backend.services.gemini_service import (
    GeminiAuthenticationError,
    generate_chat_reply,
    search_web_snippets,
)

chat_bp = Blueprint("chat", __name__)

@chat_bp.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    prompt = str(data.get("prompt", "")).strip()
    web_search = bool(data.get("web_search", False))

    if not prompt:
        return jsonify({"error": "請先輸入 prompt。"}), 400

    try:
        reply_data = generate_chat_reply(prompt, web_search=web_search)
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
