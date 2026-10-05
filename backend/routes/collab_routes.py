import random
import time
from flask import Blueprint, jsonify, request
from backend.services.collab_service import (
    MEMBER_COLORS,
    clean_stale_voice_participants,
    ensure_room_defaults,
    generate_room_code,
    rooms_cache,
    rooms_lock,
    save_room,
)
from backend.services.gemini_service import generate_chat_reply
from backend.services.music_service import (
    PRESET_MUSIC,
    handle_dj_chat,
    resolve_spotify_track,
)

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
        ensure_room_defaults(room)
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

        ensure_room_defaults(room)
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
            ensure_room_defaults(room)
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

            # 若該使用者在語音通話中，一併移除
            vc_parts = room.get("voice_channel", {}).get("participants", {})
            if user_id in vc_parts:
                del vc_parts[user_id]
                room["voice_channel"]["is_active"] = len(vc_parts) > 0

            room["updated_at"] = now
            save_room(room)
        return jsonify({"success": True})

@collab_bp.get("/api/collab/sync/<room_id>")
def collab_sync(room_id):
    room_id = room_id.strip().upper()
    since = int(request.args.get("since", 0))
    voice_since = int(request.args.get("voice_since", 0))
    user_id = request.args.get("user_id", "").strip()
    user_name = request.args.get("user_name", "").strip()

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if not room:
            return jsonify({"error": "房間不存在或已關閉"}), 404

        ensure_room_defaults(room)
        now = time.time()
        if user_id and user_id in room["members"]:
            room["members"][user_id]["last_seen"] = now
            if user_name:
                room["members"][user_id]["user_name"] = user_name

        clean_stale_voice_participants(room)

        active_members = [
            m for m in room["members"].values()
            if (now - m.get("last_seen", 0)) < 60
        ]

        new_msgs = [m for m in room["messages"] if m["id"] > since]
        latest_id = room["messages"][-1]["id"] if room["messages"] else 0

        # 語音與音樂狀態
        vc = room.get("voice_channel", {})
        voice_participants = list(vc.get("participants", {}).values())
        music = room.get("music_player", {})
        all_v_msgs = room.get("voice_messages", [])
        new_v_msgs = [m for m in all_v_msgs if m["id"] > voice_since]
        latest_v_id = all_v_msgs[-1]["id"] if all_v_msgs else 0

        return jsonify({
            "success": True,
            "room_id": room["room_id"],
            "project_name": room["project_name"],
            "project_goal": room.get("project_goal", ""),
            "creator_id": room.get("creator_id", ""),
            "members": active_members,
            "new_messages": new_msgs,
            "shared_notes": room.get("shared_notes", ""),
            "latest_message_id": latest_id,
            "voice_channel": {
                "is_active": len(voice_participants) > 0,
                "participants": voice_participants
            },
            "music_player": music,
            "new_voice_messages": new_v_msgs,
            "latest_voice_msg_id": latest_v_id
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

# ==========================================
# 語音通話 (Voice Channel) 專屬路由
# ==========================================

@collab_bp.post("/api/collab/voice/join")
def voice_join():
    data = request.get_json(silent=True) or {}
    room_id = str(data.get("room_id", "")).strip().upper()
    user_id = str(data.get("user_id", "")).strip()
    user_name = str(data.get("user_name", "")).strip() or "組員"

    if not room_id or not user_id:
        return jsonify({"error": "缺少 room_id 或 user_id"}), 400

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if not room:
            return jsonify({"error": "找不到此房間"}), 404

        ensure_room_defaults(room)
        now = time.time()
        user_color = room["members"].get(user_id, {}).get("color", "#0284c7")

        vc = room["voice_channel"]
        vc["participants"][user_id] = {
            "user_id": user_id,
            "user_name": user_name,
            "color": user_color,
            "muted": False,
            "deafened": False,
            "speaking": False,
            "joined_at": now,
            "last_ping": now
        }
        vc["is_active"] = True

        v_msg_id = len(room["voice_messages"]) + 1
        room["voice_messages"].append({
            "id": v_msg_id,
            "user_id": "system",
            "user_name": "語音頻道",
            "role": "system",
            "text": f"🎙️ 【{user_name}】已加入語音通話頻道！",
            "timestamp": now,
            "is_dj": False
        })

        room["updated_at"] = now
        save_room(room)
        return jsonify({
            "success": True,
            "voice_channel": {
                "is_active": True,
                "participants": list(vc["participants"].values())
            }
        })

@collab_bp.post("/api/collab/voice/leave")
def voice_leave():
    data = request.get_json(silent=True) or {}
    room_id = str(data.get("room_id", "")).strip().upper()
    user_id = str(data.get("user_id", "")).strip()
    user_name = str(data.get("user_name", "")).strip() or "組員"

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if room:
            ensure_room_defaults(room)
            now = time.time()
            vc = room["voice_channel"]
            if user_id in vc["participants"]:
                del vc["participants"][user_id]
                vc["is_active"] = len(vc["participants"]) > 0

                v_msg_id = len(room["voice_messages"]) + 1
                room["voice_messages"].append({
                    "id": v_msg_id,
                    "user_id": "system",
                    "user_name": "語音頻道",
                    "role": "system",
                    "text": f"👋 【{user_name}】離開了語音通話。",
                    "timestamp": now,
                    "is_dj": False
                })
                room["updated_at"] = now
                save_room(room)
        return jsonify({"success": True})

@collab_bp.post("/api/collab/voice/state")
def voice_state():
    data = request.get_json(silent=True) or {}
    room_id = str(data.get("room_id", "")).strip().upper()
    user_id = str(data.get("user_id", "")).strip()
    muted = bool(data.get("muted", False))
    deafened = bool(data.get("deafened", False))
    speaking = bool(data.get("speaking", False))

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if not room:
            return jsonify({"error": "找不到此房間"}), 404

        ensure_room_defaults(room)
        now = time.time()
        vc = room["voice_channel"]
        if user_id in vc["participants"]:
            vc["participants"][user_id]["muted"] = muted
            vc["participants"][user_id]["deafened"] = deafened
            vc["participants"][user_id]["speaking"] = speaking
            vc["participants"][user_id]["last_ping"] = now

        clean_stale_voice_participants(room)
        return jsonify({
            "success": True,
            "participants": list(vc["participants"].values())
        })

@collab_bp.post("/api/collab/voice/signal")
def voice_signal():
    """WebRTC 信令中繼交換 (offer, answer, candidate)"""
    data = request.get_json(silent=True) or {}
    room_id = str(data.get("room_id", "")).strip().upper()
    from_id = str(data.get("from_id", "")).strip()
    to_id = str(data.get("to_id", "")).strip()
    sig_type = str(data.get("type", "")).strip()
    payload = data.get("payload")

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if not room:
            return jsonify({"error": "房間不存在"}), 404

        ensure_room_defaults(room)
        vc = room["voice_channel"]
        vc["signals"].append({
            "from_id": from_id,
            "to_id": to_id,
            "type": sig_type,
            "payload": payload,
            "timestamp": time.time()
        })
        return jsonify({"success": True})

@collab_bp.get("/api/collab/voice/signals/<room_id>")
def voice_get_signals(room_id):
    room_id = room_id.strip().upper()
    user_id = request.args.get("user_id", "").strip()

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if not room:
            return jsonify({"signals": []})

        ensure_room_defaults(room)
        vc = room["voice_channel"]
        my_signals = [s for s in vc["signals"] if s.get("to_id") == user_id]
        # 取出後移除已派送給自己的信令
        vc["signals"] = [s for s in vc["signals"] if s.get("to_id") != user_id]
        return jsonify({"signals": my_signals})

# ==========================================
# 音樂播放台與 Spotify 連動專屬路由
# ==========================================

@collab_bp.get("/api/collab/music/presets")
def music_presets():
    return jsonify({"success": True, "presets": PRESET_MUSIC})

@collab_bp.get("/api/collab/music/search")
def music_search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"error": "請提供搜尋詞或 Spotify 連結"}), 400
    track = resolve_spotify_track(q)
    return jsonify({"success": True, "track": track})

@collab_bp.post("/api/collab/music/play")
def music_play():
    data = request.get_json(silent=True) or {}
    room_id = str(data.get("room_id", "")).strip().upper()
    user_id = str(data.get("user_id", "")).strip()
    user_name = str(data.get("user_name", "")).strip() or "組員"
    track_input = data.get("track")
    query = str(data.get("query", "")).strip()

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if not room:
            return jsonify({"error": "找不到此房間"}), 404

        ensure_room_defaults(room)
        if track_input and isinstance(track_input, dict):
            track = track_input
        elif query:
            track = resolve_spotify_track(query)
        else:
            track = PRESET_MUSIC[0]

        now = time.time()
        track["requested_by"] = user_name
        track["started_at"] = now

        player = room["music_player"]
        if player.get("current_track"):
            player["history"].append(player["current_track"])
            if len(player["history"]) > 20:
                player["history"].pop(0)

        player["current_track"] = track
        player["status"] = "playing"
        player["started_at"] = now

        v_msg_id = len(room["voice_messages"]) + 1
        room["voice_messages"].append({
            "id": v_msg_id,
            "user_id": "dj_bot",
            "user_name": "小白鯊 DJ 🎧",
            "role": "assistant",
            "text": f"🎧 **正在播放**：《{track['title']}》 - {track.get('artist', '精選音樂')}\n✨ 由 **{user_name}** 點播！快戴上耳機一起聽吧～🎶",
            "timestamp": now,
            "is_dj": True,
            "track": track
        })

        room["updated_at"] = now
        save_room(room)
        return jsonify({
            "success": True,
            "current_track": track,
            "music_player": player
        })

@collab_bp.post("/api/collab/music/queue")
def music_queue():
    data = request.get_json(silent=True) or {}
    room_id = str(data.get("room_id", "")).strip().upper()
    user_name = str(data.get("user_name", "")).strip() or "組員"
    track_input = data.get("track")
    query = str(data.get("query", "")).strip()

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if not room:
            return jsonify({"error": "找不到此房間"}), 404

        ensure_room_defaults(room)
        track = track_input if isinstance(track_input, dict) else resolve_spotify_track(query)
        track["requested_by"] = user_name

        player = room["music_player"]
        player["queue"].append(track)

        v_msg_id = len(room["voice_messages"]) + 1
        room["voice_messages"].append({
            "id": v_msg_id,
            "user_id": "dj_bot",
            "user_name": "小白鯊 DJ 🎧",
            "role": "assistant",
            "text": f"➕ 已將《{track['title']}》加入播放清單第 {len(player['queue'])} 首！（點播者：{user_name}）",
            "timestamp": time.time(),
            "is_dj": True,
            "track": track
        })

        room["updated_at"] = time.time()
        save_room(room)
        return jsonify({"success": True, "queue": player["queue"]})

@collab_bp.post("/api/collab/music/control")
def music_control():
    data = request.get_json(silent=True) or {}
    room_id = str(data.get("room_id", "")).strip().upper()
    action = str(data.get("action", "")).strip()

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if not room:
            return jsonify({"error": "找不到此房間"}), 404

        ensure_room_defaults(room)
        player = room["music_player"]
        now = time.time()

        if action == "pause":
            player["status"] = "paused"
        elif action == "resume" or action == "play":
            player["status"] = "playing"
        elif action == "next":
            if player["queue"]:
                next_t = player["queue"].pop(0)
                if player.get("current_track"):
                    player["history"].append(player["current_track"])
                player["current_track"] = next_t
                player["status"] = "playing"
                player["started_at"] = now
            else:
                # 隊列空時隨機推薦一首預設音樂
                next_t = random.choice(PRESET_MUSIC)
                player["current_track"] = next_t
                player["status"] = "playing"
                player["started_at"] = now
        elif action == "clear_queue":
            player["queue"] = []

        room["updated_at"] = now
        save_room(room)
        return jsonify({"success": True, "music_player": player})

# ==========================================
# 通話專屬【音樂 DJ 機器人】交互路由
# (明確不負責課業問題與搜尋功能，專注音樂與娛樂)
# ==========================================

@collab_bp.post("/api/collab/dj/chat")
def dj_chat():
    data = request.get_json(silent=True) or {}
    room_id = str(data.get("room_id", "")).strip().upper()
    user_id = str(data.get("user_id", "")).strip()
    user_name = str(data.get("user_name", "")).strip() or "組員"
    text = str(data.get("text", "")).strip()

    if not text:
        return jsonify({"error": "訊息內容不可為空。"}), 400

    with rooms_lock:
        room = rooms_cache.get(room_id)
        if not room:
            return jsonify({"error": "找不到此房間"}), 404

        ensure_room_defaults(room)
        now = time.time()

        # 紀錄使用者在通話聊天室的發言
        user_msg_id = len(room["voice_messages"]) + 1
        room["voice_messages"].append({
            "id": user_msg_id,
            "user_id": user_id,
            "user_name": user_name,
            "role": "user",
            "text": text,
            "timestamp": now,
            "is_dj": False
        })

        # 交由 DJ 音樂機器人專門處理（課業/搜尋攔截、點歌、趣味骰子/音效）
        dj_result = handle_dj_chat(text, user_name, room)
        reply_text = dj_result.get("reply", "")
        action = dj_result.get("action", "chat")
        track = dj_result.get("track")

        if action == "play" and track:
            player = room["music_player"]
            if player.get("current_track"):
                player["history"].append(player["current_track"])
            track["requested_by"] = user_name
            track["started_at"] = now
            player["current_track"] = track
            player["status"] = "playing"
            player["started_at"] = now
        elif action == "next":
            player = room["music_player"]
            if player["queue"]:
                track = player["queue"].pop(0)
                player["current_track"] = track
                player["status"] = "playing"
            else:
                track = random.choice(PRESET_MUSIC)
                player["current_track"] = track
                player["status"] = "playing"
        elif action == "pause":
            room["music_player"]["status"] = "paused"
        elif action == "resume":
            room["music_player"]["status"] = "playing"

        dj_msg_id = len(room["voice_messages"]) + 1
        room["voice_messages"].append({
            "id": dj_msg_id,
            "user_id": "dj_bot",
            "user_name": "小白鯊 DJ 🎧",
            "role": "assistant",
            "text": reply_text,
            "timestamp": time.time(),
            "is_dj": True,
            "action": action,
            "track": track
        })

        room["updated_at"] = time.time()
        save_room(room)

        return jsonify({
            "success": True,
            "reply": reply_text,
            "action": action,
            "track": track,
            "music_player": room["music_player"]
        })
