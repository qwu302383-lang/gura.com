# 🦈 Gura AI Web Assistant

> 基於 Google Gemini 3.6 Flash 的全功能 AI 智慧助理、即時聯網檢索、語音雙向互動與多人多人協同專案平台。

---

## 🌟 核心特色功能

### 1. ⚡ Google Gemini 3.6 Flash AI 推理
- 預設接入最新 `gemini-3.6-flash` 模型，具備毫秒級超高響應速度與優異的多輪對話理解能力。
- 內建智慧容錯切換清單（Fallback Models: `gemini-3.5-flash`, `gemini-2.5-flash`, `gemini-flash-latest`），服務不中斷。

### 2. 🔍 即時網路檢索增強 (Web Grounding)
- 整合 DuckDuckGo 即時搜尋引擎，隨時查詢最新網路新聞、即時資訊與事實驗證。
- 自動提取搜尋摘要並標註原始網頁來源連結。

### 3. 🎙️ 語音辨識與語音朗讀 (STT & TTS)
- **語音輸入 (STT)**：原生支援 Web Speech API，點擊麥克風即可直接以語音輸入。
- **語音播放 (TTS)**：支援文字轉語音（Text-to-Speech）語音撥放，自動濾除程式碼區塊提供自然流暢的聆聽體驗。

### 4. ⏰ 智慧手機聯動控制 (Mobile Intent Actions)
- 自動理解自然語言指令（如：「明天早上 7 點叫我起床」、「倒數 5 分鐘」、「明天下午 3 點安排專案會議」）。
- 生成專屬互動卡片，可直接呼叫 Android 原生鬧鐘、時鐘計時器或 Google 日曆活動。

### 5. 👥 多人連線即時專案協同房間 (Multiplayer Collaboration)
- **專案房間**：支援建立與加入 8 碼專案協同代碼（如 `PRJ-XXXX`）。
- **多人即時對話**：同一專案內所有成員發言自動即時同步。
- **共享便條紙 (Shared Notes)**：多人共同編輯專案待辦與備忘錄，支援防衝突同步與本地資料持久化。

### 6. 📱 手機自適應響應式佈局
- 針對手機螢幕最佳化，歷史紀錄側邊欄可一鍵收縮/展開，使對話視窗享有全螢幕視野。

### 7. 🏗️ 前後端解耦與即時狀態控制台
- 採用標準模組化架構，將後端 API 與前端 UI/靜態資源徹底分離。
- 頂部導覽列內建「即時後端狀態燈」與「前後端架構儀表板」，可即時檢測連線 Ping 延遲（毫秒）與運算狀態。

---

## 📁 專案架構目錄

```text
├── backend/                        # ⚡ 後端模組 (Flask API & Services)
│   ├── routes/                     # Blueprint 路由切分
│   │   ├── chat_routes.py          # /api/chat (對話與聯網搜尋)
│   │   ├── collab_routes.py        # /api/collab/* (多人協同專案房間)
│   │   ├── system_routes.py        # /api/system/status, /api/system/ping
│   │   └── main_routes.py          # 前端入口
│   ├── services/                   # 核心邏輯
│   │   ├── gemini_service.py       # Gemini 3.6 Flash 與 Google Search 封裝
│   │   └── collab_service.py       # 專案房間引擎與持久化
│   ├── config.py                   # 後端環境配置
│   └── __init__.py                 # Flask Application Factory
│
├── frontend/                       # 💻 前端介面與客戶端資源
│   ├── templates/index.html        # 網頁結構與架構控制台
│   └── static/
│       ├── app.js                  # 前端狀態機、語音、協同控制器
│       └── style.css               # 樣式表與動態效果
│
├── app.py                          # 應用程式進入點 (Application Entry)
├── run_server.py                   # 本地服務與 Cloudflare Tunnel 啟動器
├── render.yaml                     # Render 雲端平台部署設定
├── requirements.txt                # Python 依賴清單
├── Procfile                        # 雲端容器啟動命令
└── ARCHITECTURE.md                 # 系統架構圖與 API 規格文檔
```

---

## 🚀 快速開始

### 1. 本地環境運行

1. **安裝依賴套件**：
   ```bash
   pip install -r requirements.txt
   ```

2. **設定環境變數**：
   複製 `.env.example` 為 `.env`，並填入您的 Gemini API 金鑰：
   ```ini
   GEMINI_API_KEY=你的_Google_Gemini_API_Key
   GEMINI_MODEL=gemini-3.6-flash
   ```

3. **啟動伺服器**：
   ```bash
   python app.py
   ```
   瀏覽器開啟：`http://localhost:5000`

### 2. 本地穿透對外公開網址 (Cloudflare Tunnel)

若希望讓手機或其他遠端裝置免安裝連線：
```bash
python run_server.py
```
程式會自動啟動後端並建立 Cloudflare 穿透，在終端機與 `public_url.txt` 輸出專屬的公網 HTTPS 網址。

### 3. 部署至 Render 雲端平台 (24/7 永久在線)

1. 將專案推送到您的 GitHub 倉庫。
2. 前往 [Render.com](https://render.com) 建立 **Web Service**，選擇此倉庫。
3. 環境變數設定：
   - `GEMINI_API_KEY`: 填入您的 Google AI Studio API Key。
   - `GEMINI_MODEL`: `gemini-3.6-flash`
4. 部署完成後，即可獲得永久 24 小時在線的專屬公網網址！

---

## 📄 授權條款

本專案採用 MIT License 開源授權。
