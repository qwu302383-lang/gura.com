import os
import requests

# 自動載入專案目錄下的 .env 檔案
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(ENV_PATH):
    try:
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip("'\"")
                    if k:
                        os.environ[k] = v
    except Exception:
        pass

import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

DEFAULT_API_KEY = ""
API_KEY = os.getenv("GEMINI_API_KEY", "").strip() or DEFAULT_API_KEY
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash").strip()

FALLBACK_MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest",
]


class GeminiAuthenticationError(RuntimeError):
    """Gemini API key is invalid or not authorized for the API."""


def _mask_key(text, key):
    if key and key in text:
        return text.replace(key, "[KEY_PROTECTED]")
    return text


def search_web_snippets(query, max_results=4):
    """即時網路檢索：快速獲取網頁摘要與標題，供 Gemini 聯網引用"""
    if not query or len(query.strip()) < 2:
        return []

    # 移除鬧鐘/計時器等純指令字眼，專注於知識/事實檢索
    clean_q = re.sub(r'(幫我|請|查詢|搜尋|搜尋一下|查一下)', '', query).strip()
    if not clean_q:
        clean_q = query

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    }
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(clean_q)
    req = urllib.request.Request(url, headers=headers)

    results = []
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            # 匹配標題與連結
            title_matches = re.findall(r'<a class="result__url"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html)
            snippet_matches = re.findall(r'<a class="result__snippet[^"]*"[^>]*>(.*?)</a>', html)

            for i in range(min(len(snippet_matches), max_results)):
                raw_snippet = snippet_matches[i]
                clean_snippet = re.sub(r"<[^>]+>", "", raw_snippet).strip()

                raw_url = ""
                raw_title = clean_q
                if i < len(title_matches):
                    raw_url = title_matches[i][0].strip()
                    raw_title = re.sub(r"<[^>]+>", "", title_matches[i][1]).strip()

                # 解碼 DuckDuckGo 重定向 URL
                if "uddg=" in raw_url:
                    try:
                        raw_url = urllib.parse.unquote(raw_url.split("uddg=")[1].split("&")[0])
                    except Exception:
                        pass

                if clean_snippet:
                    results.append({
                        "title": raw_title or f"網路搜尋結果 #{i+1}",
                        "snippet": clean_snippet,
                        "url": raw_url if raw_url.startswith("http") else f"https://www.google.com/search?q={urllib.parse.quote(clean_q)}"
                    })
    except Exception as e:
        print(f"Web search exception: {e}")

    return results


def detect_phone_actions(prompt):
    """解析語意中是否包含手機 App 動作（鬧鐘、計時器、行事曆提醒）"""
    if not prompt:
        return None

    text = prompt.strip()

    # 1. 鬧鐘辨識 (Alarm)
    if any(k in text for k in ["鬧鐘", "叫我", "叫醒", "設定鬧鐘", "設鬧鐘"]):
        m = re.search(r'(明天|後天)?\s*(早上|上午|下午|晚上|凌晨|半夜|清晨)?\s*(\d{1,2})\s*(?:[:點時點鐘]\s*(\d{1,2})?|點半)?', text)
        if m:
            day_str = m.group(1) or ""
            period = m.group(2) or ""
            hour = int(m.group(3))
            minute = 0
            if "半" in text[m.start():m.end() + 2]:
                minute = 30
            elif m.group(4):
                minute = int(m.group(4))

            if period in ("下午", "晚上") and hour < 12:
                hour += 12
            elif period in ("凌晨", "早上", "上午", "清晨") and hour == 12:
                hour = 0

            # 抓取鬧鐘標籤或備註
            label = re.sub(r'(幫我|請|設定|設|個|的|鬧鐘|叫我|起床|在|時間)', '', text).strip()
            if not label or len(label) > 20:
                label = "Gura 提醒鬧鐘"

            time_str = f"{hour:02d}:{minute:02d}"
            intent_url = (
                f"intent:#Intent;action=android.intent.action.SET_ALARM;"
                f"i.android.intent.extra.HOUR={hour};"
                f"i.android.intent.extra.MINUTES={minute};"
                f"S.android.intent.extra.MESSAGE={urllib.parse.quote(label)};"
                f"B.android.intent.extra.SKIP_UI=false;end"
            )

            return {
                "type": "alarm",
                "title": f"⏰ 手機鬧鐘：{day_str} {time_str}",
                "time_str": time_str,
                "hour": hour,
                "minute": minute,
                "label": label,
                "intent_url": intent_url,
                "action_hint": "點擊可在手機鬧鐘 App 自動建立此鬧鐘，或在此網頁直接響鈴。"
            }

    # 2. 倒數計時器辨識 (Timer)
    if any(k in text for k in ["計時", "倒數", "定時", "計時器", "倒數計時"]):
        m = re.search(r'(\d+)\s*(秒鐘|秒|分鐘|分|小時|hr|min|sec)', text)
        if m:
            val = int(m.group(1))
            unit = m.group(2)
            if "秒" in unit or "sec" in unit:
                sec = val
                time_display = f"{sec} 秒"
            elif "小" in unit or "hr" in unit:
                sec = val * 3600
                time_display = f"{val} 小時"
            else:
                sec = val * 60
                time_display = f"{val} 分鐘"

            label = re.sub(r'(幫我|請|設定|設|倒數|計時|器|個)', '', text).strip()
            if not label or len(label) > 20:
                label = f"{time_display}計時"

            intent_url = (
                f"intent:#Intent;action=android.intent.action.SET_TIMER;"
                f"i.android.intent.extra.LENGTH={sec};"
                f"S.android.intent.extra.MESSAGE={urllib.parse.quote(label)};"
                f"B.android.intent.extra.SKIP_UI=false;end"
            )

            return {
                "type": "timer",
                "title": f"⏱️ 倒數計時器：{time_display}",
                "seconds": sec,
                "time_display": time_display,
                "label": label,
                "intent_url": intent_url,
                "action_hint": "點擊可在手機時鐘 App 啟動倒數，或在網頁直接啟動音效計時。"
            }

    # 3. 行事曆行程 (Calendar)
    if any(k in text for k in ["行事曆", "日程", "安排行程", "會議", "加到日曆", "提醒事項"]):
        clean_title = re.sub(r'(加到行事曆|加到日曆|排程|安排|提醒我)', '', text).strip()
        if not clean_title:
            clean_title = "新行程事項"

        now = datetime.now()
        start_time = now + timedelta(hours=1)
        end_time = start_time + timedelta(hours=1)
        dates_param = f"{start_time.strftime('%Y%m%dT%H%M00')}/{end_time.strftime('%Y%m%dT%H%M00')}"
        gcal_url = (
            f"https://calendar.google.com/calendar/render?action=TEMPLATE&"
            f"text={urllib.parse.quote(clean_title)}&"
            f"dates={dates_param}&"
            f"details={urllib.parse.quote('來自 Gura 助理排程')}"
        )

        return {
            "type": "calendar",
            "title": f"📅 日曆排程：{clean_title}",
            "label": clean_title,
            "gcal_url": gcal_url,
            "action_hint": "點擊直接開啟 Google 日曆或手機行事曆 App 建立活動。"
        }

    return None


def generate_chat_reply(prompt, web_search=False):
    """呼叫 Gemini 產生對話，同時支援網路檢索增強與手機指令卡片生成"""
    api_key = os.getenv("GEMINI_API_KEY", "").strip() or API_KEY
    if not api_key:
        raise GeminiAuthenticationError(
            "請先設定有效的 GEMINI_API_KEY；請到 Google AI Studio 建立新金鑰。"
        )

    # 檢測手機聯動動作
    phone_action = detect_phone_actions(prompt)

    # 檢測或執行網路檢索
    search_sources = []
    augmented_instruction = "請使用繁體中文回答，專有名詞可保留英文。"

    if web_search:
        search_sources = search_web_snippets(prompt, max_results=4)
        if search_sources:
            snippets_text = "\n".join(
                [f"[{i+1}] {s['title']}: {s['snippet']} (來源: {s['url']})" for i, s in enumerate(search_sources)]
            )
            augmented_instruction += (
                f"\n\n【即時網路檢索資訊】\n以下為系統為此問題檢索到的最新網路資料：\n{snippets_text}\n"
                "請結合上述即時資訊回答使用者，並在回答中提及最新資訊。"
            )

    preferred_model = os.getenv("GEMINI_MODEL", "").strip() or MODEL or "gemini-3.6-flash"
    models_to_try = [preferred_model] + [m for m in FALLBACK_MODELS if m != preferred_model]

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }

    payload = {
        "systemInstruction": {
            "parts": [{"text": augmented_instruction}]
        },
        "contents": [{"parts": [{"text": prompt}]}],
    }

    last_error = None

    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        for attempt in range(2):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=45)
                if response.status_code == 200:
                    result = response.json()
                    candidates = result.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts and "text" in parts[0]:
                            return {
                                "response": parts[0]["text"],
                                "search_sources": search_sources,
                                "phone_action": phone_action,
                            }
                elif response.status_code in (401, 403):
                    raise GeminiAuthenticationError(
                        "Gemini API 金鑰無效或未授權（HTTP "
                        f"{response.status_code}）。請撤銷外洩的舊金鑰，建立新金鑰並更新 GEMINI_API_KEY。"
                    )
                elif response.status_code == 404:
                    last_error = f"模型 {model} 不存在或目前不可用 (HTTP 404)，切換備用模型中..."
                    break
                elif response.status_code in (500, 503, 504, 429):
                    last_error = f"模型 {model} 暫時負載過高 (HTTP {response.status_code})，切換備用模型中..."
                    break
                else:
                    detail = response.text[:300].replace("\n", " ")
                    raise RuntimeError(f"Gemini API 回傳 HTTP {response.status_code}: {detail}")
            except requests.exceptions.Timeout:
                last_error = f"模型 {model} 連線逾時，切換備用模型中..."
                break
            except GeminiAuthenticationError:
                raise
            except Exception as e:
                err_str = _mask_key(str(e), api_key)
                last_error = f"模型 {model} 發生錯誤: {err_str}"
                break

    clean_err = _mask_key(str(last_error or "未知錯誤"), api_key)
    raise RuntimeError(f"Gemini 請求失敗：{clean_err}")


def generate_response(prompt, web_search=False):
    """相容舊版介面的函式，直接回傳純文字回覆"""
    data = generate_chat_reply(prompt, web_search=web_search)
    return data["response"]
