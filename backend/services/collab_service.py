import json
import os
import random
import string
import time
from threading import Lock
from backend.config import ROOMS_DIR
from backend.services.music_service import PRESET_MUSIC

rooms_lock = Lock()
rooms_cache = {}

MEMBER_COLORS = [
    "#0284c7", "#10b981", "#8b5cf6", "#f59e0b",
    "#ec4899", "#06b6d4", "#f97316", "#14b8a6"
]

def ensure_room_defaults(room: dict):
    """確保房間資料包含最新語音通話與音樂播放器狀態欄位"""
    now = time.time()
    
    if "voice_channel" not in room or not isinstance(room["voice_channel"], dict):
        room["voice_channel"] = {
            "is_active": False,
            "participants": {},
            "signals": []
        }
    else:
        if "participants" not in room["voice_channel"]:
            room["voice_channel"]["participants"] = {}
        if "signals" not in room["voice_channel"]:
            room["voice_channel"]["signals"] = []

    if "music_player" not in room or not isinstance(room["music_player"], dict):
        room["music_player"] = {
            "current_track": None,
            "status": "idle",
            "queue": [],
            "history": [],
            "started_at": 0,
            "volume": 80
        }
    else:
        # 若當前未在播放具體點播歌曲，維持待機靜音，點進 DJ 時不主動播放
        if not room["music_player"].get("current_track"):
            room["music_player"]["status"] = "idle"
            room["music_player"]["current_track"] = None

    if "voice_messages" not in room or not isinstance(room["voice_messages"], list):
        room["voice_messages"] = [
            {
                "id": 1,
                "user_id": "dj_bot",
                "user_name": "小白鯊 DJ 🎧",
                "role": "assistant",
                "text": "🎧 歡迎來到通話頻道！我是專屬音樂 DJ 小白鯊！我不負責課業解題與資料搜尋喔～目前尚未播放音樂，請在下方輸入欄輸入想聽的歌名（例如：「我想聽 晴天」或貼上 Spotify 連結），我立刻為大家播歌！🎶",
                "timestamp": now,
                "is_dj": True
            }
        ]
        
    return room

def clean_stale_voice_participants(room: dict):
    """清除超過 25 秒無心跳的語音成員與過期信令"""
    now = time.time()
    vc = room.get("voice_channel", {})
    participants = vc.get("participants", {})
    
    stale_ids = [uid for uid, p in participants.items() if (now - p.get("last_ping", 0)) > 25]
    for uid in stale_ids:
        del participants[uid]
        
    vc["is_active"] = len(participants) > 0
    
    # 清除 30 秒前的 WebRTC 信令
    if "signals" in vc and isinstance(vc["signals"], list):
        vc["signals"] = [s for s in vc["signals"] if (now - s.get("timestamp", 0)) < 30]

def load_all_rooms():
    global rooms_cache
    with rooms_lock:
        if os.path.exists(ROOMS_DIR):
            for fname in os.listdir(ROOMS_DIR):
                if fname.endswith(".json"):
                    fpath = os.path.join(ROOMS_DIR, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            room = json.load(f)
                            ensure_room_defaults(room)
                            clean_stale_voice_participants(room)
                            rooms_cache[room["room_id"]] = room
                    except Exception as e:
                        print(f"Error loading room {fname}: {e}")

load_all_rooms()

def save_room(room):
    room_id = room["room_id"]
    ensure_room_defaults(room)
    clean_stale_voice_participants(room)
    rooms_cache[room_id] = room
    fpath = os.path.join(ROOMS_DIR, f"{room_id}.json")
    try:
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(room, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving room {room_id}: {e}")

def generate_room_code():
    chars = string.ascii_uppercase + string.digits
    for _ in range(30):
        code = "PRJ-" + "".join(random.choices(chars, k=4))
        if code not in rooms_cache:
            return code
    return "PRJ-" + "".join(random.choices(chars, k=6))

def get_room(room_id):
    with rooms_lock:
        r = rooms_cache.get(room_id.upper())
        if r:
            ensure_room_defaults(r)
        return r

def get_rooms_count():
    with rooms_lock:
        return len(rooms_cache)
