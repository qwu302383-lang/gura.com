import json
import os
import random
import string
import time
from threading import Lock
from backend.config import ROOMS_DIR

rooms_lock = Lock()
rooms_cache = {}

MEMBER_COLORS = [
    "#0284c7", "#10b981", "#8b5cf6", "#f59e0b",
    "#ec4899", "#06b6d4", "#f97316", "#14b8a6"
]

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
                            rooms_cache[room["room_id"]] = room
                    except Exception as e:
                        print(f"Error loading room {fname}: {e}")

load_all_rooms()

def save_room(room):
    room_id = room["room_id"]
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
        return rooms_cache.get(room_id.upper())

def get_rooms_count():
    with rooms_lock:
        return len(rooms_cache)
