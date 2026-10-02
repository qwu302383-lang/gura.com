import random
import time
from flask import Blueprint, jsonify, request
from backend.services.collab_service import (
    MEMBER_COLORS,
    generate_room_code,
    rooms_cache,
    rooms_lock,
    save_room,
)
from backend.services.gemini_service import generate_chat_reply

collab_bp = Blueprint("collab", __name__)

@collab_bp.post("/api/collab/create")
def collab_create():
    data = request.get_json(silent=True) or {}
    project_name = str(data.get("project_name", "")).strip() or "未命名協作專案"
    project_goal = str(data.get("project_goal", "")).strip()
    creator_name = str(data.get("creator_name", "")).strip() or "主揪人"
    user_id = str(data.get("user_id", "")).strip() or f"user_{int(time.time()*1000)}"

    with rooms_lock:
        room_id = generate_room_code()
        now = time.time()
        room = {
            "room_id": room_id,
            "project_name": project_name,
            "project_goal": project_goal,
            "created_at": now,
            "updated_at": now,
            "creator_id": user_id,
            "creator_name": creator_name,
            "members": {
                user_id: {
                    "user_id": user_id,
                    "user_name": creator_name,
                    "is_host": True,
                    "last_seen": now,
                    "color": MEMBER_COLORS[0]
                }
            },
            "messages": [
                {
                    "id": 1,
                    "user_id": "system",
                    "user_name": "系統通知",
                    "role": "system",
                    "text": f"🎉 專案【{project_name}】連機協作室已建立！歡迎大家一起討論。",
                    "timestamp": now,
                    "is_ai": False
                }
            ],
            "shared_notes": f"# 📌 {project_name}\n\n**🎯 專案目標**：{project_goal or '共同討論並產出最佳成果'}\n\n## 💡 討論共識與紀錄\n- \n\n## ✅ 待辦任務分工\n- [ ] "
        }
        save_room(room)
        return jsonify({"success": True, "room": room})

@collab_bp.post("/api/collab/join")
def collab_join():
    data = request.get_json(silent=True) or {}
    raw_code = str(data.get("room_id", "")).strip().upper()
    user_name = str(data.get("user_name", "")).strip() or "組員"
    user_id = str(data.get("user_id", "")).strip() or f"user_{int(time.time()*1000)}"

    if "ROOM=" in raw_code:
        raw_code = raw_code.split("ROOM=")[-1].split("&")[0].strip()
    if not raw_code.startswith("PRJ-") and len(raw_code) == 4:
        raw_code = f"PRJ-{raw_code}"

    with rooms_lock:
        room = rooms_cache.get(raw_code)
        if not room:
            return jsonify({"error": f"找不到房間代碼「{raw_code}」，請確認後重試。"}), 404

        now = time.time()
        existing_colors = [m.get("color") for m in room["members"].values()]
        available_colors = [c for c in MEMBER_COLORS if c not in existing_colors]
        chosen_color = available_colors[0] if available_colors else random.choice(MEMBER_COLORS)

        is_new_join = user_id not in room["members"]
        room["members"][user_id] = {
            "user_id": user_id,
            "user_name": user_name,
            "is_host": room.get("creator_id") == user_id,
            "last_seen": now,
            "color": chosen_color
        }

        if is_new_join:
            next_id = len(room["messages"]) + 1
            room["messages"].append({
                "id": next_id,
                "user_id": "system",
                "user_name": "系統通知",
                "role": "system",
                "text": f"👋 成員【{user_name}】加入了專案連機討論！",
                "timestamp": now,
                "is_ai": False
            })

        room["updated_at"] = now
        save_room(room)
        return jsonify({"success": True, "room": room})

@collab_bp.post("/api/collab/leave")
def collab_leave():
    data = request.get_json(silent=True) or {}
    room_id = str(data.get("room_id", "")).strip().upper()
    user_id = str(data.get("user_id", "")).strip()
    user_name = str(data.get("user_name", "")).strip() or "組員"

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if room:
            now = time.time()
            if user_id in room["members"]:
                del room["members"][user_id]
                next_id = len(room["messages"]) + 1
                room["messages"].append({
                    "id": next_id,
                    "user_id": "system",
                    "user_name": "系統通知",
                    "role": "system",
                    "text": f"👋 成員【{user_name}】離開了專案連機。",
                    "timestamp": now,
                    "is_ai": False
                })
                room["updated_at"] = now
                save_room(room)
        return jsonify({"success": True})

@collab_bp.get("/api/collab/sync/<room_id>")
def collab_sync(room_id):
    room_id = room_id.strip().upper()
    since = int(request.args.get("since", 0))
    user_id = request.args.get("user_id", "").strip()
    user_name = request.args.get("user_name", "").strip()

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if not room:
            return jsonify({"error": "房間不存在或已關閉"}), 404

        now = time.time()
        if user_id and user_id in room["members"]:
            room["members"][user_id]["last_seen"] = now
            if user_name:
                room["members"][user_id]["user_name"] = user_name

        active_members = [
            m for m in room["members"].values()
            if (now - m.get("last_seen", 0)) < 60
        ]

        new_msgs = [m for m in room["messages"] if m["id"] > since]
        latest_id = room["messages"][-1]["id"] if room["messages"] else 0

        return jsonify({
            "success": True,
            "room_id": room["room_id"],
            "project_name": room["project_name"],
            "project_goal": room.get("project_goal", ""),
            "creator_id": room.get("creator_id", ""),
            "members": active_members,
            "new_messages": new_msgs,
            "shared_notes": room.get("shared_notes", ""),
            "latest_message_id": latest_id
        })

@collab_bp.post("/api/collab/message")
def collab_message():
    data = request.get_json(silent=True) or {}
    room_id = str(data.get("room_id", "")).strip().upper()
    user_id = str(data.get("user_id", "")).strip()
    user_name = str(data.get("user_name", "")).strip() or "組員"
    text = str(data.get("text", "")).strip()
    web_search = bool(data.get("web_search", False))
    trigger_ai = bool(data.get("trigger_ai", True))

    if not text:
        return jsonify({"error": "訊息內容不可為空。"}), 400

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if not room:
            return jsonify({"error": "找不到此連機房間。"}), 404

        now = time.time()
        user_color = room["members"].get(user_id, {}).get("color", "#0284c7")
        next_id = len(room["messages"]) + 1
        user_msg = {
            "id": next_id,
            "user_id": user_id,
            "user_name": user_name,
            "role": "user",
            "text": text,
            "timestamp": now,
            "color": user_color,
            "is_ai": False
        }
        room["messages"].append(user_msg)
        room["updated_at"] = now
        save_room(room)

    ai_msg = None
    if trigger_ai:
        try:
            context_prompt = f"【團隊專案連機討論 - 專案名稱：{room['project_name']}】\n提問成員：{user_name}\n\n內容：{text}"
            reply_data = generate_chat_reply(context_prompt, web_search=web_search)
            ai_text = reply_data.get("response", "")

            with rooms_lock:
                if room_id in rooms_cache:
                    room = rooms_cache[room_id]
                    now = time.time()
                    ai_id = len(room["messages"]) + 1
                    ai_msg = {
                        "id": ai_id,
                        "user_id": "gemini_ai",
                        "user_name": "Gemini 3.6 Flash",
                        "role": "assistant",
                        "text": ai_text,
                        "timestamp": now,
                        "is_ai": True,
                        "search_sources": reply_data.get("search_sources", [])
                    }
                    room["messages"].append(ai_msg)
                    room["updated_at"] = now
                    save_room(room)
        except Exception as e:
            with rooms_lock:
                if room_id in rooms_cache:
                    room = rooms_cache[room_id]
                    err_id = len(room["messages"]) + 1
                    room["messages"].append({
                        "id": err_id,
                        "user_id": "system",
                        "user_name": "系統提示",
                        "role": "system",
                        "text": f"⚠️ Gemini AI 回覆失敗：{str(e)}",
                        "timestamp": time.time(),
                        "is_ai": False
                    })
                    save_room(room)

    return jsonify({
        "success": True,
        "user_message": user_msg,
        "ai_message": ai_msg
    })

@collab_bp.post("/api/collab/notes")
def collab_notes():
    data = request.get_json(silent=True) or {}
    room_id = str(data.get("room_id", "")).strip().upper()
    notes = str(data.get("notes", ""))

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if not room:
            return jsonify({"error": "找不到此連機房間。"}), 404
        room["shared_notes"] = notes
        room["updated_at"] = time.time()
        save_room(room)
        return jsonify({"success": True, "shared_notes": notes})
