import re
import urllib.parse
import random
import time
import requests

DEFAULT_AUDIO_FALLBACK = "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/47/f5/24/47f5242d-9171-e807-b377-32093badcd42/mzaf_14678549351252112301.plus.aac.p.m4a"

# 精選熱門與專注推薦音樂庫 (附真實 Spotify ID、封面與可直接播放之音訊串流)
PRESET_MUSIC = [
    {
        "id": "0bYg9bo50gSsH3LtWvIm5K",
        "title": "Lofi Hip Hop - 讀書專注音樂",
        "artist": "Lofi Fruits Music",
        "category": "專注讀書",
        "spotify_url": "https://open.spotify.com/track/0bYg9bo50gSsH3LtWvIm5K",
        "spotify_embed_url": "https://open.spotify.com/embed/track/0bYg9bo50gSsH3LtWvIm5K?utm_source=generator&theme=0",
        "cover_url": "https://image-cdn-ak.spotifycdn.com/image/ab67616d00001e028b19aa15a81e9f1a04ec4a87",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/47/f5/24/47f5242d-9171-e807-b377-32093badcd42/mzaf_14678549351252112301.plus.aac.p.m4a"
    },
    {
        "id": "4cOdK2wGLETKBW3PvgPWqT",
        "title": "Never Gonna Give You Up",
        "artist": "Rick Astley",
        "category": "歐美經典",
        "spotify_url": "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT",
        "spotify_embed_url": "https://open.spotify.com/embed/track/4cOdK2wGLETKBW3PvgPWqT?utm_source=generator&theme=0",
        "cover_url": "https://image-cdn-ak.spotifycdn.com/image/ab67616d00001e02baf89eb11ec7c657805d2da0",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/62/ff/3a/62ff3abe-bc6d-a7d0-31b0-71cbec9aaa24/mzaf_13802296211720217737.plus.aac.p.m4a"
    },
    {
        "id": "0VjIjW4GlUZAMYd2vXMi3b",
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "category": "熱門榜單",
        "spotify_url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
        "spotify_embed_url": "https://open.spotify.com/embed/track/0VjIjW4GlUZAMYd2vXMi3b?utm_source=generator&theme=0",
        "cover_url": "https://image-cdn-ak.spotifycdn.com/image/ab67616d00001e028863bc11d2aa12b54f5aeb36",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/12/73/ca/1273ca46-233a-5331-189b-25ac1d656533/mzaf_976341070785891411.plus.aac.p.m4a"
    },
    {
        "id": "7qiZfU4dY1lWllzX7mPBI3",
        "title": "Shape of You",
        "artist": "Ed Sheeran",
        "category": "流行熱播",
        "spotify_url": "https://open.spotify.com/track/7qiZfU4dY1lWllzX7mPBI3",
        "spotify_embed_url": "https://open.spotify.com/embed/track/7qiZfU4dY1lWllzX7mPBI3?utm_source=generator&theme=0",
        "cover_url": "https://image-cdn-ak.spotifycdn.com/image/ab67616d00001e02ba5db46f4b838ef6027e6f96",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/44/c7/4f/44c74f0d-72dc-6143-d4d0-ba14d661ca0d/mzaf_9566898362556366703.plus.aac.p.m4a"
    },
    {
        "id": "3dPtQ0d7L9Mei3b9q4M6qP",
        "title": "夜に駆ける (Racing into the Night)",
        "artist": "YOASOBI",
        "category": "動漫日韓",
        "spotify_url": "https://open.spotify.com/track/3dPtQ0d7L9Mei3b9q4M6qP",
        "spotify_embed_url": "https://open.spotify.com/embed/track/3dPtQ0d7L9Mei3b9q4M6qP?utm_source=generator&theme=0",
        "cover_url": "https://image-cdn-ak.spotifycdn.com/image/ab67616d00001e02c6114a070eb0326077ff0a89",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/41/5e/b0/415eb064-77c4-0195-210e-ddc80f3c984d/mzaf_7767226104050015250.plus.aac.p.m4a"
    },
    {
        "id": "5s7LwV3mS4z9Wf5n3N5z8x",
        "title": "如果可以 (Red Scarf)",
        "artist": "韋禮安 WeiBird",
        "category": "華語抒情",
        "spotify_url": "https://open.spotify.com/track/5s7LwV3mS4z9Wf5n3N5z8x",
        "spotify_embed_url": "https://open.spotify.com/embed/track/5s7LwV3mS4z9Wf5n3N5z8x?utm_source=generator&theme=0",
        "cover_url": "https://image-cdn-ak.spotifycdn.com/image/ab67616d00001e02cbdb82e753c15d5e1ff74ec0",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/ed/07/65/ed07651a-f348-3b7c-4aba-d666b3606946/mzaf_5806429344424646657.plus.aac.p.m4a"
    },
    {
        "id": "303W52K0A5Lq4l8tW1A00j",
        "title": "晴天",
        "artist": "周杰倫",
        "category": "華語金曲",
        "spotify_url": "https://open.spotify.com/track/303W52K0A5Lq4l8tW1A00j",
        "spotify_embed_url": "https://open.spotify.com/embed/track/303W52K0A5Lq4l8tW1A00j?utm_source=generator&theme=0",
        "cover_url": "https://image-cdn-ak.spotifycdn.com/image/ab67616d00001e0267eb49a8837e4299b9c02ff4",
        "preview_url": "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/20/d0/e7/20d0e7db-9c12-795a-d738-2fc3dde4ac9a/mzaf_10317517925583301645.plus.aac.p.m4a"
    }
]

# 課業/作業/解題 與 搜尋 關鍵字過濾庫 (嚴格拒絕)
ACADEMIC_KEYWORDS = [
    "作業", "功課", "考試", "題目", "數學", "英文", "物理", "化學", "生物", "歷史", "地理",
    "解題", "算式", "解答", "幫我寫", "作文", "期末", "期中", "論文", "程式作業", "代碼作業",
    "debug", "寫程式", "程式碼", "翻譯這段", "問答題", "選擇題", "證明題", "背誦", "筆記整理"
]

SEARCH_KEYWORDS = [
    "搜尋", "搜索", "google", "查資料", "查新聞", "新聞", "今天天氣", "股票",
    "誰是", "什麼是", "為什麼", "查一下", "幫我查", "wikipedia", "維基百科", "最新消息"
]

def check_academic_or_search(query: str):
    """
    檢查用戶訊息是否涉及課業問題或資訊搜尋。
    若涉及，傳回 True 及拒絕原因。
    """
    q = query.lower().strip()
    
    # 判斷是否為課業問題
    for kw in ACADEMIC_KEYWORDS:
        if kw in q:
            return True, "academic", kw
            
    # 判斷是否為網路搜尋
    for kw in SEARCH_KEYWORDS:
        if kw in q:
            return True, "search", kw
            
    return False, None, None

def search_itunes_preview(query: str):
    """透過 iTunes 搜尋取得音訊串流與專輯封面"""
    try:
        # 中文查詢時優先使用台灣市場代碼，提高命中率
        has_cjk = any('\u4e00' <= char <= '\u9fff' for char in query)
        country_param = "&country=TW" if has_cjk else ""
        itunes_url = f"https://itunes.apple.com/search?term={urllib.parse.quote(query)}&entity=song&limit=1{country_param}"
        res = requests.get(itunes_url, timeout=3)
        if res.status_code == 200:
            results = res.json().get("results", [])
            if results:
                top = results[0]
                return {
                    "title": top.get("trackName"),
                    "artist": top.get("artistName"),
                    "cover_url": top.get("artworkUrl100", "").replace("100x100bb", "600x600bb"),
                    "preview_url": top.get("previewUrl")
                }
    except Exception:
        pass
    return None

def resolve_spotify_track(input_text: str):
    """
    解析用戶輸入的文字或連結：
    1. 若為 Spotify 網址或 URI，自動提取 track ID 並抓取 oEmbed 封面與資訊，同時搭配可播放音訊。
    2. 若為歌名或歌手，先比對內建資料庫；若無則透過 iTunes 搜尋取得真實音訊與專輯封面，並產生 Spotify 連結。
    """
    clean_text = input_text.strip()
    
    # 1. 檢查是否為 Spotify Track / Playlist / Album 連結
    spotify_track_match = re.search(r'spotify\.com/(?:[a-zA-Z-]+/)?track/([a-zA-Z0-9]{22})', clean_text)
    if not spotify_track_match:
        spotify_track_match = re.search(r'spotify:track:([a-zA-Z0-9]{22})', clean_text)
        
    if spotify_track_match:
        track_id = spotify_track_match.group(1)
        spotify_url = f"https://open.spotify.com/track/{track_id}"
        embed_url = f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0"
        title = f"Spotify Track ({track_id})"
        artist = "Spotify 藝人"
        cover_url = ""
        preview_url = ""
        
        # 嘗試利用 Spotify oEmbed 獲取詳細資訊
        try:
            r = requests.get(f"https://open.spotify.com/oembed?url={spotify_url}", timeout=3)
            if r.status_code == 200:
                data = r.json()
                title = data.get("title", title)
                cover_url = data.get("thumbnail_url", "")
                if " by " in title:
                    parts = title.split(" by ")
                    title = parts[0]
                    artist = parts[1]
                    
                # 依曲名搜尋真實試聽音檔
                itunes_info = search_itunes_preview(f"{artist} {title}")
                if itunes_info and itunes_info.get("preview_url"):
                    preview_url = itunes_info["preview_url"]
        except Exception:
            pass
            
        return {
            "id": track_id,
            "title": title,
            "artist": artist,
            "spotify_url": spotify_url,
            "spotify_embed_url": embed_url,
            "cover_url": cover_url,
            "preview_url": preview_url or DEFAULT_AUDIO_FALLBACK,
            "source": "spotify_direct"
        }

    # 檢查 Spotify Playlist 連結
    spotify_playlist_match = re.search(r'spotify\.com/(?:[a-zA-Z-]+/)?playlist/([a-zA-Z0-9]{22})', clean_text)
    if spotify_playlist_match:
        pl_id = spotify_playlist_match.group(1)
        sp_url = f"https://open.spotify.com/playlist/{pl_id}"
        return {
            "id": pl_id,
            "title": "Spotify 精選播放清單",
            "artist": "Spotify Playlist",
            "spotify_url": sp_url,
            "spotify_embed_url": f"https://open.spotify.com/embed/playlist/{pl_id}?utm_source=generator&theme=0",
            "cover_url": "",
            "preview_url": DEFAULT_AUDIO_FALLBACK,
            "source": "spotify_playlist"
        }

    # 2. 比對內建推薦清單
    for p in PRESET_MUSIC:
        if (p["title"].lower() in clean_text.lower() or 
            p["artist"].lower() in clean_text.lower() or
            clean_text.lower() in p["title"].lower() or
            (p["category"].lower() in clean_text.lower() and len(clean_text) <= 6)):
            return dict(p)

    # 3. 嘗試以 iTunes API 搜尋歌曲元數據（名稱、藝人、專輯封面、真實音訊串流）
    search_query = clean_text
    for prefix in ["我想聽", "請播", "播放", "點歌", "放一下", "放首", "來首", "播", "聽"]:
        if search_query.startswith(prefix):
            search_query = search_query[len(prefix):].strip()
            
    itunes_info = search_itunes_preview(search_query)
    if itunes_info:
        t_title = itunes_info.get("title") or search_query
        t_artist = itunes_info.get("artist") or "精選歌手"
        artwork = itunes_info.get("cover_url") or ""
        preview_mp3 = itunes_info.get("preview_url") or DEFAULT_AUDIO_FALLBACK
        
        spotify_search_link = f"https://open.spotify.com/search/{urllib.parse.quote(f'{t_artist} {t_title}')}"
        
        return {
            "id": f"song_{int(time.time()*1000)}",
            "title": t_title,
            "artist": t_artist,
            "spotify_url": spotify_search_link,
            "spotify_embed_url": PRESET_MUSIC[0]["spotify_embed_url"],
            "cover_url": artwork,
            "preview_url": preview_mp3,
            "source": "search"
        }

    # 4. 找不到時的安全兜底（保證絕對有聲音播放）
    safe_q = clean_text or "好聽音樂"
    return {
        "id": f"custom_{int(time.time())}",
        "title": safe_q,
        "artist": "自選點播",
        "spotify_url": f"https://open.spotify.com/search/{urllib.parse.quote(safe_q)}",
        "spotify_embed_url": PRESET_MUSIC[0]["spotify_embed_url"],
        "cover_url": "",
        "preview_url": DEFAULT_AUDIO_FALLBACK,
        "source": "custom_search"
    }

def handle_dj_chat(text: str, user_name: str, room: dict):
    """
    處理語音通話內【專屬音樂 DJ 機器人】的聊天與點播互動：
    - 嚴格拒絕處理課業問題與網路搜尋！
    - 支援音樂點播、推薦歌單、切歌、音量以及趣味骰子/音效。
    """
    clean_text = text.strip()
    
    # 1. 嚴格過濾：若包含課業問題或搜尋功能，堅決拒絕並指引至主對話區
    is_blocked, block_type, keyword = check_academic_or_search(clean_text)
    if is_blocked:
        if block_type == "academic":
            refusal_text = (
                f"🚫 **抱歉喔！我是通話音樂專屬 DJ【小白鯊 DJ】🎧**\n\n"
                f"我不負責處理「課業解題、功課作業或學術問答」喔（偵測到課業關鍵字：`{keyword}`）！\n\n"
                f"💡 **建議操作**：\n"
                f"請切換至【主聊天室】向 **Gura AI 主助理** 提問，Gura 會為你提供最完整的解答與分析！\n\n"
                f"🎶 **在通話頻道裡，我專門為大家放音樂與熱鬧氣氛！** 快跟我點一首喜歡的歌吧～例如「我想聽 晴天」或貼上 Spotify 連結！"
            )
        else:
            refusal_text = (
                f"🚫 **抱歉喔！我是通話音樂專屬 DJ【小白鯊 DJ】🎧**\n\n"
                f"我不負責處理「即時資訊搜尋與網路檢索」喔（偵測到搜尋關鍵字：`{keyword}`）！\n\n"
                f"💡 **建議操作**：\n"
                f"請至【主聊天室】開啟「聯網搜尋」並詢問 **Gura AI 主助理**，即可獲得即時搜尋結果！\n\n"
                f"🎶 **在通話頻道裡，我的職責是音樂點播與娛樂陪伴！** 想聽抒情歌、Lo-Fi 還是熱門流行曲呢？隨時跟我說！"
            )
        return {
            "success": True,
            "action": "refusal",
            "reply": refusal_text,
            "track": None
        }

    # 2. 趣味骰子 / 抽籤 / 決定功能
    dice_match = re.search(r'(骰子|擲骰|抽籤|誰先|決定誰|roll)', clean_text.lower())
    if dice_match:
        dice_num = random.randint(1, 6)
        dice_reply = (
            f"🎲 **【DJ 幸運骰子】響起！**\n\n"
            f"叮鈴鈴～DJ 替大家擲出了骰子：【 **{dice_num}** 點】！\n"
            f"🎉 點數最大的朋友或對應第 {dice_num} 位組員，輪到你開麥分享囉～大家繼續保持好心情！"
        )
        return {
            "success": True,
            "action": "dice",
            "reply": dice_reply,
            "track": None
        }

    # 3. 歡呼鼓掌 / DJ 氣氛音效
    cheer_match = re.search(r'(歡呼|鼓掌|掌聲|慶祝|乾杯|讚|加油|太棒了)', clean_text.lower())
    if cheer_match:
        cheer_reply = (
            f"👏 **【DJ 現場音效開播】** 📣\n\n"
            f"*(嘩啦啦啦～現場響起熱烈的歡呼與掌聲音效！)*\n"
            f"🎉 **{user_name}** 與各位組員太棒了！大家專案進度超前，DJ 給你們按一個大大的讚！繼續衝刺！💪"
        )
        return {
            "success": True,
            "action": "sound_effect",
            "reply": cheer_reply,
            "track": None
        }

    # 4. 音樂切歌 / 暫停 / 下一首
    if any(k in clean_text.lower() for k in ["下一首", "切歌", "next", "跳過"]):
        return {
            "success": True,
            "action": "next",
            "reply": "⏭️ **收到指令！** DJ 正在切換至下一首待播歌曲～🎧",
            "track": None
        }
        
    if any(k in clean_text.lower() for k in ["暫停", "pause", "停一下"]):
        return {
            "success": True,
            "action": "pause",
            "reply": "⏸️ **音樂已暫停。** 想繼續收聽時對我說「播放」即可！",
            "track": None
        }

    if any(k in clean_text.lower() for k in ["繼續", "播放", "play", "resume"]) and len(clean_text) <= 4:
        return {
            "success": True,
            "action": "resume",
            "reply": "▶️ **音樂繼續播放中！** 戴上耳機，一同享受音樂與討論吧～🎶",
            "track": None
        }

    # 5. 音樂點播或推薦請求
    music_keywords = ["聽", "播", "放", "歌", "曲", "音樂", "spotify", "點歌", "lofi", "推薦", "抒情", "熱門"]
    is_music_request = any(kw in clean_text.lower() for kw in music_keywords) or ("spotify.com" in clean_text)
    
    if is_music_request:
        track = resolve_spotify_track(clean_text)
        reply_msg = (
            f"🎧 **【DJ 已為大家點播】《{track['title']}》**\n\n"
            f"🎤 **歌手 / 演出**：{track.get('artist', '精選音樂')}\n"
            f"✨ 由組員 **{user_name}** 熱情點播！已加入房間音樂台播放～\n"
            f"🟢 瀏覽器正直接播放高音質試聽，亦可點擊下方【在 Spotify 開啟】同步收藏！🎶"
        )
        return {
            "success": True,
            "action": "play",
            "reply": reply_msg,
            "track": track
        }

    # 6. 一般問候或閒聊（DJ 身份設定）
    default_reply = (
        f"🎧 **嗨嗨 {user_name}！我是通話音樂專屬 DJ 小白鯊！**\n\n"
        f"我的職責是專為聯機通話提供：\n"
        f"- 🎵 **Spotify 音樂點播**（告訴我歌名或貼上 Spotify 連結）\n"
        f"- ☕ **精選背景音樂**（Lo-Fi 專注、華語金曲、歐美熱播）\n"
        f"- 🎲 **會議抽籤 / 擲骰子**（決定誰先發言報告）\n\n"
        f"⚠️ *提醒：我不負責課業解題與資料搜尋喔！課業相關請至主聊天室詢問 Gura AI 主助理。*\n\n"
        f"現在想聽什麼歌呢？直接輸入歌名跟我說吧！"
    )
    return {
        "success": True,
        "action": "chat",
        "reply": default_reply,
        "track": None
    }
