// DOM 元素選取
const form = document.querySelector('#chatForm');
const input = document.querySelector('#promptInput');
const messages = document.querySelector('#messages');
const sendButton = document.querySelector('#sendButton');
const clearButton = document.querySelector('#clearButton');
const newChatButton = document.querySelector('#newChatButton');
const clearHistoryButton = document.querySelector('#clearHistoryButton');
const historyList = document.querySelector('#historyList');
const historySearchInput = document.querySelector('#historySearchInput');
const historySearchClearBtn = document.querySelector('#historySearchClearBtn');
const sessionLabel = document.querySelector('#sessionLabel');
const sessionTitle = document.querySelector('#sessionTitle');

// 語音與拓展工具列元素
const voiceInputBtn = document.querySelector('#voiceInputBtn');
const voiceInputStatus = document.querySelector('#voiceInputStatus');
const autoSpeakToggleBtn = document.querySelector('#autoSpeakToggleBtn');
const autoSpeakBadge = document.querySelector('#autoSpeakBadge');
const webSearchToggleBtn = document.querySelector('#webSearchToggleBtn');
const webSearchBadge = document.querySelector('#webSearchBadge');

// 連機協作相關 DOM 元素
const collabButton = document.querySelector('#collabButton');
const collabButtonText = document.querySelector('#collabButtonText');
const collabStatusDot = document.querySelector('#collabStatusDot');
const sidebarCollabBtn = document.querySelector('#sidebarCollabBtn');
const sidebarCollabCountBadge = document.querySelector('#sidebarCollabCountBadge');

const collabBanner = document.querySelector('#collabBanner');
const collabBannerProjectName = document.querySelector('#collabBannerProjectName');
const collabBannerRoomCode = document.querySelector('#collabBannerRoomCode');
const collabAvatarStack = document.querySelector('#collabAvatarStack');
const collabMemberCountText = document.querySelector('#collabMemberCountText');
const collabInviteBtn = document.querySelector('#collabInviteBtn');
const collabNotesBtn = document.querySelector('#collabNotesBtn');
const collabLeaveBtn = document.querySelector('#collabLeaveBtn');

const collabModal = document.querySelector('#collabModal');
const closeCollabModal = document.querySelector('#closeCollabModal');
const collabEntryView = document.querySelector('#collabEntryView');
const collabActiveView = document.querySelector('#collabActiveView');

const collabTabCreateBtn = document.querySelector('#collabTabCreateBtn');
const collabTabJoinBtn = document.querySelector('#collabTabJoinBtn');
const collabCreateTab = document.querySelector('#collabCreateTab');
const collabJoinTab = document.querySelector('#collabJoinTab');

const collabCreateNameInput = document.querySelector('#collabCreateNameInput');
const collabCreateGoalInput = document.querySelector('#collabCreateGoalInput');
const collabCreateNicknameInput = document.querySelector('#collabCreateNicknameInput');
const startCollabCreateBtn = document.querySelector('#startCollabCreateBtn');

const collabJoinCodeInput = document.querySelector('#collabJoinCodeInput');
const collabJoinNicknameInput = document.querySelector('#collabJoinNicknameInput');
const startCollabJoinBtn = document.querySelector('#startCollabJoinBtn');

const collabActiveProjectTitle = document.querySelector('#collabActiveProjectTitle');
const collabActiveProjectGoal = document.querySelector('#collabActiveProjectGoal');
const collabActiveRoomCode = document.querySelector('#collabActiveRoomCode');
const copyCollabCodeBtn = document.querySelector('#copyCollabCodeBtn');
const collabActiveShareUrl = document.querySelector('#collabActiveShareUrl');
const copyCollabUrlBtn = document.querySelector('#copyCollabUrlBtn');
const collabQrImg = document.querySelector('#collabQrImg');
const collabActiveMemberCount = document.querySelector('#collabActiveMemberCount');
const collabActiveMemberList = document.querySelector('#collabActiveMemberList');

const collabNotesStatus = document.querySelector('#collabNotesStatus');
const collabSharedNotesInput = document.querySelector('#collabSharedNotesInput');
const saveCollabNotesBtn = document.querySelector('#saveCollabNotesBtn');
const exitCollabRoomBtn = document.querySelector('#exitCollabRoomBtn');

// 登入相關元素
const loginButton = document.querySelector('#loginButton');
const userProfile = document.querySelector('#userProfile');
const userAvatar = document.querySelector('#userAvatar');
const userAvatarImg = document.querySelector('#userAvatarImg');
const userName = document.querySelector('#userName');
const logoutButton = document.querySelector('#logoutButton');
const loginModal = document.querySelector('#loginModal');
const closeLoginModal = document.querySelector('#closeLoginModal');
const googlePrimaryAccountBtn = document.querySelector('#googlePrimaryAccountBtn');
const googleUseOtherBtn = document.querySelector('#googleUseOtherBtn');
const googleRemoveAccountBtn = document.querySelector('#googleRemoveAccountBtn');
const googleAccountsBox = document.querySelector('#googleAccountsBox');
const googleOtherForm = document.querySelector('#googleOtherForm');
const googleCustomEmail = document.querySelector('#googleCustomEmail');
const googleCustomName = document.querySelector('#googleCustomName');
const googleCancelOtherBtn = document.querySelector('#googleCancelOtherBtn');
const googleSignInBtnContainer = document.querySelector('#googleSignInBtnContainer');

// SVG 圖標
const COPY_ICON_SVG = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>`;
const EDIT_ICON_SVG = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path></svg>`;
const TRASH_ICON_SVG = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>`;
const SPEAKER_ICON_SVG = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>`;
const SPEAKER_STOP_ICON_SVG = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="12" height="12" rx="2" fill="currentColor"></rect></svg>`;

// Storage 鍵名
const SESSIONS_KEY = 'prompt_atelier_sessions';
const USER_KEY = 'prompt_atelier_user';
const GOOGLE_CLIENT_ID_KEY = 'prompt_atelier_google_client_id';
const AUTO_SPEAK_KEY = 'gura_auto_speak_enabled';
const WEB_SEARCH_KEY = 'gura_web_search_enabled';
const COLLAB_ROOM_KEY = 'gura_collab_room_id';
const COLLAB_USER_ID_KEY = 'gura_collab_user_id';
const COLLAB_NICKNAME_KEY = 'gura_collab_nickname';

// 當前會話 ID
let currentSessionId = null;

// ==========================================
// 1. 登入 / 身份模組（含 Google 第三方登入）
// ==========================================
function getUser() {
  try {
    return JSON.parse(localStorage.getItem(USER_KEY));
  } catch (e) {
    return null;
  }
}

function setUser(user) {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
  updateAuthUI();
}

function removeUser() {
  localStorage.removeItem(USER_KEY);
  updateAuthUI();
}

function updateAuthUI() {
  const user = getUser();
  const googleBadge = document.querySelector('#googleBadge');
  const userEmail = document.querySelector('#userEmail');

  if (user && user.name) {
    loginButton.style.display = 'none';
    userProfile.style.display = 'flex';
    userName.textContent = user.name;

    if (userEmail) {
      userEmail.textContent = user.email || '';
      userEmail.style.display = user.email ? 'block' : 'none';
    }

    if (googleBadge) {
      googleBadge.style.display = user.provider === 'google' ? 'grid' : 'none';
    }

    if (user.picture) {
      userAvatarImg.src = user.picture;
      userAvatarImg.style.display = 'block';
      userAvatar.style.display = 'none';
    } else {
      userAvatarImg.style.display = 'none';
      userAvatar.style.display = 'grid';
      userAvatar.textContent = user.name.slice(0, 1).toUpperCase();
    }
  } else {
    loginButton.style.display = 'inline-flex';
    userProfile.style.display = 'none';
  }

  // 同步側邊欄底部使用者資訊
  const sidebarUserName = document.querySelector('#sidebarUserName');
  const sidebarUserAvatarImg = document.querySelector('#sidebarUserAvatarImg');
  const sidebarUserAvatarFallback = document.querySelector('#sidebarUserAvatarFallback');

  if (sidebarUserName) {
    sidebarUserName.textContent = user ? user.name : '吳奕璿';
  }
  if (sidebarUserAvatarImg && sidebarUserAvatarFallback) {
    if (user && user.picture) {
      sidebarUserAvatarImg.src = user.picture;
      sidebarUserAvatarImg.style.display = 'block';
      sidebarUserAvatarFallback.style.display = 'none';
    } else {
      sidebarUserAvatarImg.src = '/static/google_avatar.png';
      sidebarUserAvatarImg.style.display = 'block';
      sidebarUserAvatarFallback.style.display = 'none';
    }
  }
}

function openLoginModal() {
  loginModal.style.display = 'flex';
  if (googleAccountsBox) googleAccountsBox.style.display = 'block';
  if (googleOtherForm) googleOtherForm.style.display = 'none';
  if (googleCustomEmail) googleCustomEmail.value = '';
  if (googleCustomName) googleCustomName.value = '';
  initGoogleAuth();
}

function closeLoginModalFunc() {
  loginModal.style.display = 'none';
}

// 解析 Google JWT Token
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    console.error('Failed to parse Google JWT', e);
    return null;
  }
}

// Google 授權成功回調
function handleGoogleCredentialResponse(response) {
  const data = parseJwt(response.credential);
  if (!data) return;

  const user = {
    name: data.name || data.email,
    email: data.email,
    picture: data.picture,
    provider: 'google',
    loginTime: Date.now()
  };

  setUser(user);
  closeLoginModalFunc();
}

// 初始化 Google Identity Services
function initGoogleAuth() {
  const clientId = (window.ENV_GOOGLE_CLIENT_ID && window.ENV_GOOGLE_CLIENT_ID !== 'None') 
    ? window.ENV_GOOGLE_CLIENT_ID 
    : (localStorage.getItem(GOOGLE_CLIENT_ID_KEY) || '');

  if (window.google && window.google.accounts && clientId) {
    try {
      google.accounts.id.initialize({
        client_id: clientId,
        callback: handleGoogleCredentialResponse,
        auto_select: false
      });

      if (googleSignInBtnContainer) {
        googleSignInBtnContainer.innerHTML = '';
        google.accounts.id.renderButton(googleSignInBtnContainer, {
          theme: 'outline',
          size: 'large',
          text: 'continue_with',
          shape: 'rectangular',
          width: 320
        });
        if (googleCustomBtn) googleCustomBtn.style.display = 'none';
      }
    } catch (err) {
      console.warn('Google Identity Services 初始化警告:', err);
    }
  }
}

if (googlePrimaryAccountBtn) {
  googlePrimaryAccountBtn.addEventListener('click', () => {
    setUser({
      name: '413076吳奕璿',
      email: 'hs413076@ms.nnkieh.tn.edu.tw',
      picture: '/static/google_avatar.png',
      provider: 'google',
      loginTime: Date.now()
    });
    closeLoginModalFunc();
  });
}

if (googleUseOtherBtn) {
  googleUseOtherBtn.addEventListener('click', () => {
    if (googleAccountsBox) googleAccountsBox.style.display = 'none';
    if (googleOtherForm) {
      googleOtherForm.style.display = 'flex';
      if (googleCustomEmail) googleCustomEmail.focus();
    }
  });
}

if (googleCancelOtherBtn) {
  googleCancelOtherBtn.addEventListener('click', () => {
    if (googleOtherForm) googleOtherForm.style.display = 'none';
    if (googleAccountsBox) googleAccountsBox.style.display = 'block';
  });
}

if (googleOtherForm) {
  googleOtherForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = googleCustomEmail.value.trim();
    if (!email) return;
    const name = googleCustomName.value.trim() || email.split('@')[0];
    setUser({
      name,
      email,
      picture: '/static/google_avatar.png',
      provider: 'google',
      loginTime: Date.now()
    });
    closeLoginModalFunc();
  });
}

if (googleRemoveAccountBtn) {
  googleRemoveAccountBtn.addEventListener('click', () => {
    removeUser();
    closeLoginModalFunc();
  });
}

if (loginButton) loginButton.addEventListener('click', openLoginModal);
if (closeLoginModal) closeLoginModal.addEventListener('click', closeLoginModalFunc);
if (logoutButton) logoutButton.addEventListener('click', removeUser);

if (loginModal) {
  loginModal.addEventListener('click', (e) => {
    if (e.target === loginModal) closeLoginModalFunc();
  });
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && loginModal && loginModal.style.display === 'flex') {
    closeLoginModalFunc();
  }
});

window.addEventListener('load', () => {
  let count = 0;
  const timer = setInterval(() => {
    count++;
    if ((window.google && window.google.accounts) || count > 20) {
      clearInterval(timer);
      initGoogleAuth();
    }
  }, 200);
});

// ==========================================
// 2. 歷史紀錄 & 會話模組
// ==========================================
function getSessions() {
  try {
    const raw = localStorage.getItem(SESSIONS_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    return [];
  }
}

function saveSessions(sessions) {
  localStorage.setItem(SESSIONS_KEY, JSON.stringify(sessions));
}

function formatHistoryTime(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();
  const diffMs = now - date;
  const diffMinutes = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMinutes / 60);

  if (diffMinutes < 1) return '剛剛';
  if (diffMinutes < 60) return `${diffMinutes} 分鐘前`;
  if (diffHours < 24 && date.getDate() === now.getDate()) {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `今天 ${hours}:${minutes}`;
  }
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${month}/${day}`;
}

function appendMessageToCurrentSession(role, text) {
  const sessions = getSessions();
  let session = sessions.find((s) => s.id === currentSessionId);

  if (!session) {
    const cleanTitle = text.replace(/[\r\n]+/g, ' ').trim().slice(0, 20) || '新對話';
    session = {
      id: 'sess_' + Date.now(),
      title: cleanTitle,
      createdAt: Date.now(),
      updatedAt: Date.now(),
      messages: []
    };
    currentSessionId = session.id;
    sessions.unshift(session);
    if (sessionTitle) sessionTitle.textContent = session.title;
    if (sessionLabel) sessionLabel.textContent = 'CONVERSATION';
  }

  session.messages.push({ role, text });
  session.updatedAt = Date.now();
  saveSessions(sessions);
  renderHistoryList();
}

function updateSessionMessage(oldPrompt, newPrompt, newResponse) {
  if (!currentSessionId) return;
  const sessions = getSessions();
  const session = sessions.find((s) => s.id === currentSessionId);
  if (!session) return;

  const msgIndex = session.messages.findIndex((m) => m.role === 'user' && m.text === oldPrompt);
  if (msgIndex !== -1) {
    session.messages[msgIndex].text = newPrompt;
    if (session.messages[msgIndex + 1] && session.messages[msgIndex + 1].role === 'assistant') {
      session.messages[msgIndex + 1].text = newResponse;
    }
  }

  if (msgIndex === 0) {
    session.title = newPrompt.replace(/[\r\n]+/g, ' ').trim().slice(0, 20) || session.title;
    if (sessionTitle) sessionTitle.textContent = session.title;
  }

  session.updatedAt = Date.now();
  saveSessions(sessions);
  renderHistoryList();
}

function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function highlightSearchMatch(text, query) {
  if (!query || !text) return escapeHtml(text || '');
  const safeText = escapeHtml(text);
  const safeQuery = escapeHtml(query);
  const regex = new RegExp(`(${escapeRegex(safeQuery)})`, 'gi');
  return safeText.replace(regex, '<mark class="search-highlight">$1</mark>');
}

function extractSnippet(text, query) {
  if (!text || !query) return '';
  const lower = text.toLowerCase();
  const lowerQuery = query.toLowerCase();
  const idx = lower.indexOf(lowerQuery);
  if (idx === -1) return '';
  
  const start = Math.max(0, idx - 14);
  const end = Math.min(text.length, idx + query.length + 24);
  let snippet = text.slice(start, end).replace(/[\r\n]+/g, ' ');
  if (start > 0) snippet = '...' + snippet;
  if (end < text.length) snippet = snippet + '...';
  return snippet;
}

function renderHistoryList(customQuery) {
  if (!historyList) return;
  const sessions = getSessions();
  const rawQuery = (typeof customQuery === 'string' ? customQuery : (historySearchInput ? historySearchInput.value : '')).trim();
  const query = rawQuery.toLowerCase();

  if (historySearchClearBtn) {
    historySearchClearBtn.style.display = rawQuery ? 'block' : 'none';
  }

  if (sessions.length === 0) {
    historyList.innerHTML = `
      <div class="history-empty">
        <div class="empty-icon">💬</div>
        <p>尚無歷史紀錄</p>
        <span>開始提問即可自動儲存</span>
      </div>
    `;
    return;
  }

  let filtered = [];

  if (!query) {
    filtered = sessions.map(s => ({ session: s, matchedSnippet: null }));
  } else {
    sessions.forEach(session => {
      const titleMatch = session.title && session.title.toLowerCase().includes(query);
      let matchedSnippet = null;

      if (Array.isArray(session.messages)) {
        for (const msg of session.messages) {
          if (msg.text && msg.text.toLowerCase().includes(query)) {
            matchedSnippet = extractSnippet(msg.text, rawQuery);
            break;
          }
        }
      }

      if (titleMatch || matchedSnippet) {
        filtered.push({ session, matchedSnippet });
      }
    });
  }

  if (query && filtered.length === 0) {
    historyList.innerHTML = `
      <div class="history-empty">
        <div class="empty-icon">🔍</div>
        <p>找不到相關對話</p>
        <span>未找到包含「${escapeHtml(rawQuery)}」的對話或訊息</span>
      </div>
    `;
    return;
  }

  historyList.innerHTML = '';
  filtered.forEach(({ session, matchedSnippet }) => {
    const item = document.createElement('div');
    item.className = `history-item ${session.id === currentSessionId ? 'active' : ''}`;
    item.dataset.id = session.id;

    const displayTitle = query ? highlightSearchMatch(session.title, rawQuery) : escapeHtml(session.title);
    let snippetHtml = '';
    if (matchedSnippet) {
      snippetHtml = `<div class="history-item-snippet" title="${escapeHtml(matchedSnippet)}">💬 ${highlightSearchMatch(matchedSnippet, rawQuery)}</div>`;
    }

    item.innerHTML = `
      <div class="history-item-content">
        <div class="history-item-title" title="${escapeHtml(session.title)}">${displayTitle}</div>
        ${snippetHtml}
        <div class="history-item-time">${formatHistoryTime(session.updatedAt)}</div>
      </div>
      <button class="history-item-del" type="button" title="刪除此紀錄" aria-label="刪除此紀錄">
        ${TRASH_ICON_SVG}
      </button>
    `;

    item.addEventListener('click', (e) => {
      if (e.target.closest('.history-item-del')) return;
      loadSession(session.id);
    });

    const delBtn = item.querySelector('.history-item-del');
    delBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      deleteSession(session.id);
    });

    historyList.appendChild(item);
  });
}

if (historySearchInput) {
  historySearchInput.addEventListener('input', () => {
    renderHistoryList();
  });
}

if (historySearchClearBtn) {
  historySearchClearBtn.addEventListener('click', () => {
    if (historySearchInput) {
      historySearchInput.value = '';
      historySearchInput.focus();
    }
    renderHistoryList('');
  });
}

function loadSession(id) {
  if (typeof collabController !== 'undefined' && collabController && collabController.isInRoom()) {
    if (!confirm('目前正在連機協作房間中，是否要先退出連機專案並切換回個人對話？')) {
      return;
    }
    collabController.leaveRoom(false);
  }
  if (typeof voiceSynthesisController !== 'undefined' && voiceSynthesisController) voiceSynthesisController.stop();
  if (typeof voiceInputController !== 'undefined' && voiceInputController) voiceInputController.stop();
  const sessions = getSessions();
  const session = sessions.find((s) => s.id === id);
  if (!session) return;

  currentSessionId = id;
  messages.innerHTML = '';

  let lastUserMsgEl = null;
  session.messages.forEach((msg) => {
    const el = addMessage(msg.role, msg.text);
    if (msg.role === 'user') {
      lastUserMsgEl = el;
    } else if (msg.role === 'assistant' && lastUserMsgEl) {
      lastUserMsgEl.pairedResponse = el;
    }
  });

  if (sessionTitle) sessionTitle.textContent = session.title;
  if (sessionLabel) sessionLabel.textContent = 'CONVERSATION';
  renderHistoryList();
  if (typeof closeMobileSidebar === 'function') closeMobileSidebar();
}

function startNewSession(skipCollabCheck = false) {
  if (!skipCollabCheck && typeof collabController !== 'undefined' && collabController && collabController.isInRoom()) {
    if (!confirm('目前正在連機協作房間中，是否要先退出連機專案並開始新對話？')) {
      return;
    }
    collabController.leaveRoom(false);
  }
  if (typeof voiceSynthesisController !== 'undefined' && voiceSynthesisController) voiceSynthesisController.stop();
  if (typeof voiceInputController !== 'undefined' && voiceInputController) voiceInputController.stop();
  if (typeof closeMobileSidebar === 'function') closeMobileSidebar();
  currentSessionId = null;
  messages.innerHTML = `
    <div class="welcome-message">
      <div class="welcome-number">01</div>
      <div>
        <h3>今天想一起完成什麼？</h3>
        <p>輸入你的問題、草稿或一個模糊的念頭。這裡會把它接住。</p>
      </div>
    </div>
  `;
  if (sessionTitle) sessionTitle.textContent = '歡迎使用gura';
  if (sessionLabel) sessionLabel.textContent = 'NEW SESSION';
  renderHistoryList();
  if (input) input.focus();
}

function deleteSession(id) {
  let sessions = getSessions();
  sessions = sessions.filter((s) => s.id !== id);
  saveSessions(sessions);

  if (currentSessionId === id) {
    startNewSession();
  } else {
    renderHistoryList();
  }
}

function clearAllHistory() {
  if (!confirm('確定要清空所有歷史對話紀錄嗎？')) return;
  saveSessions([]);
  startNewSession();
}

if (newChatButton) newChatButton.addEventListener('click', startNewSession);
if (clearButton) clearButton.addEventListener('click', startNewSession);
if (clearHistoryButton) clearHistoryButton.addEventListener('click', clearAllHistory);

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ==========================================
// 3. 訊息渲染、複製與編輯功能
// ==========================================
function copyText(text, tooltipEl) {
  const showFeedback = () => {
    if (!tooltipEl) return;
    const originalText = tooltipEl.textContent;
    tooltipEl.textContent = '已複製！';
    tooltipEl.classList.add('show-force');
    setTimeout(() => {
      tooltipEl.textContent = originalText;
      tooltipEl.classList.remove('show-force');
    }, 1500);
  };

  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(showFeedback).catch(() => fallbackCopy(text, showFeedback));
  } else {
    fallbackCopy(text, showFeedback);
  }
}

function fallbackCopy(text, callback) {
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.select();
  try {
    document.execCommand('copy');
    if (callback) callback();
  } catch (err) {
    console.error('Copy failed:', err);
  } finally {
    document.body.removeChild(textarea);
  }
}

// ==========================================
// 4. 語音輸入 (STT) 與 語音播放 (TTS) 控制器
// ==========================================
function stripMarkdownForSpeech(text) {
  if (!text) return '';
  let clean = text;
  clean = clean.replace(/```[\s\S]*?```/g, '，請參閱畫面上的程式碼。');
  clean = clean.replace(/`([^`]+)`/g, '$1');
  clean = clean.replace(/!\[(.*?)\]\(.*?\)/g, '$1');
  clean = clean.replace(/\[(.*?)\]\(.*?\)/g, '$1');
  clean = clean.replace(/#{1,6}\s+/g, '');
  clean = clean.replace(/(\*\*|__)(.*?)\1/g, '$2');
  clean = clean.replace(/(\*|_)(.*?)\1/g, '$2');
  clean = clean.replace(/^[\s]*[-*+]\s+/gm, '');
  clean = clean.replace(/^[\s]*\d+\.\s+/gm, '');
  clean = clean.replace(/^>\s+/gm, '');
  clean = clean.replace(/https?:\/\/\S+/g, '相關連結');
  clean = clean.replace(/\n+/g, '，');
  return clean.trim();
}

class VoiceSynthesisController {
  constructor() {
    this.synth = window.speechSynthesis;
    this.currentUtterance = null;
    this.currentButton = null;
    this.currentTooltip = null;
    this.voices = [];

    if (this.synth) {
      this.loadVoices();
      if (typeof this.synth.onvoiceschanged !== 'undefined') {
        this.synth.onvoiceschanged = () => this.loadVoices();
      }
    }
  }

  loadVoices() {
    if (!this.synth) return;
    this.voices = this.synth.getVoices();
  }

  getPreferredVoice() {
    if (!this.voices || this.voices.length === 0) {
      this.loadVoices();
    }
    const matchers = [
      (v) => v.lang === 'zh-TW' || v.lang === 'zh_TW' || v.lang === 'cmn-Hant-TW',
      (v) => (v.lang.startsWith('zh') || v.lang.startsWith('cmn')) && (v.name.includes('Taiwan') || v.name.includes('Traditional') || v.name.includes('國語') || v.name.includes('Hanhan')),
      (v) => v.lang === 'zh-HK' || v.lang === 'zh_HK',
      (v) => v.lang.startsWith('zh') || v.lang.startsWith('cmn'),
    ];

    for (const matcher of matchers) {
      const found = this.voices.find(matcher);
      if (found) return found;
    }
    return null;
  }

  isPlaying() {
    return this.synth && (this.synth.speaking || this.synth.pending);
  }

  stop() {
    if (this.synth) {
      this.synth.cancel();
    }
    this.resetActiveButton();
    this.currentUtterance = null;
  }

  resetActiveButton() {
    if (this.currentButton) {
      this.currentButton.classList.remove('playing');
      this.currentButton.innerHTML = SPEAKER_ICON_SVG;
      if (this.currentTooltip) {
        this.currentTooltip.textContent = '朗讀回覆';
      }
      this.currentButton = null;
      this.currentTooltip = null;
    }
  }

  toggle(text, buttonEl, tooltipEl) {
    if (!this.synth) {
      alert('您的瀏覽器暫不支援語音播放功能。');
      return;
    }

    if (this.isPlaying() && this.currentButton === buttonEl) {
      this.stop();
      return;
    }

    this.play(text, buttonEl, tooltipEl);
  }

  play(text, buttonEl, tooltipEl) {
    if (!this.synth) return;

    this.stop();

    const cleanText = stripMarkdownForSpeech(text);
    if (!cleanText) return;

    const utterance = new SpeechSynthesisUtterance(cleanText);
    const voice = this.getPreferredVoice();
    if (voice) {
      utterance.voice = voice;
      utterance.lang = voice.lang;
    } else {
      utterance.lang = 'zh-TW';
    }

    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    this.currentUtterance = utterance;
    this.currentButton = buttonEl || null;
    this.currentTooltip = tooltipEl || null;

    if (this.currentButton) {
      this.currentButton.classList.add('playing');
      this.currentButton.innerHTML = SPEAKER_STOP_ICON_SVG;
      if (this.currentTooltip) {
        this.currentTooltip.textContent = '停止朗讀';
      }
    }

    utterance.onend = () => {
      this.resetActiveButton();
      this.currentUtterance = null;
    };

    utterance.onerror = (e) => {
      console.warn('Speech synthesis ended/interrupted:', e);
      this.resetActiveButton();
      this.currentUtterance = null;
    };

    this.synth.speak(utterance);
  }
}

class VoiceInputController {
  constructor(inputEl, btnEl, statusEl) {
    this.inputEl = inputEl;
    this.btnEl = btnEl;
    this.statusEl = statusEl;
    this.recognition = null;
    this.isListening = false;
    this.baseText = '';

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.lang = 'zh-TW';
      this.recognition.continuous = true;
      this.recognition.interimResults = true;

      this.recognition.onstart = () => {
        this.isListening = true;
        if (this.btnEl) {
          this.btnEl.classList.add('recording');
          this.btnEl.title = '正在聆聽語音中... 再次點擊即可停止';
        }
        if (this.statusEl) {
          this.statusEl.textContent = '聆聽中...';
        }
      };

      this.recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        if (finalTranscript) {
          this.baseText = (this.baseText ? this.baseText + ' ' : '') + finalTranscript.trim();
        }

        const fullDisplay = (this.baseText ? this.baseText + ' ' : '') + interimTranscript;
        if (this.inputEl && fullDisplay.trim()) {
          this.inputEl.value = fullDisplay.trim();
          this.inputEl.scrollTop = this.inputEl.scrollHeight;
        }
      };

      this.recognition.onerror = (event) => {
        console.warn('SpeechRecognition error:', event.error);
        if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
          alert('請至瀏覽器網址列設定允許存取麥克風權限，以使用語音輸入。');
        }
        this.stop();
      };

      this.recognition.onend = () => {
        this.isListening = false;
        if (this.btnEl) {
          this.btnEl.classList.remove('recording');
          this.btnEl.title = '點擊開始語音輸入（國語 / 繁體中文，再次點擊結束）';
        }
        if (this.statusEl) {
          this.statusEl.textContent = '語音輸入';
        }
      };
    }
  }

  isSupported() {
    return !!this.recognition;
  }

  start() {
    if (!this.recognition) {
      alert('您的瀏覽器暫不支援 Web Speech 語音輸入 API，建議使用 Google Chrome 或 Microsoft Edge 瀏覽器。');
      return;
    }
    if (voiceSynthesisController) {
      voiceSynthesisController.stop();
    }
    this.baseText = this.inputEl ? this.inputEl.value.trim() : '';
    try {
      this.recognition.start();
    } catch (e) {
      console.warn('Recognition start exception:', e);
      setTimeout(() => {
        try { this.recognition.start(); } catch (err) {}
      }, 200);
    }
  }

  stop() {
    if (this.recognition && this.isListening) {
      try {
        this.recognition.stop();
      } catch (e) {
        console.warn('Recognition stop exception:', e);
      }
    }
    this.isListening = false;
    if (this.btnEl) {
      this.btnEl.classList.remove('recording');
      this.btnEl.title = '點擊開始語音輸入（國語 / 繁體中文，再次點擊結束）';
    }
    if (this.statusEl) {
      this.statusEl.textContent = '語音輸入';
    }
  }

  toggle() {
    if (this.isListening) {
      this.stop();
    } else {
      this.start();
    }
  }
}

const voiceSynthesisController = new VoiceSynthesisController();
const voiceInputController = new VoiceInputController(input, voiceInputBtn, voiceInputStatus);

function isAutoSpeakEnabled() {
  return localStorage.getItem(AUTO_SPEAK_KEY) === 'true';
}

function setAutoSpeakEnabled(enabled) {
  localStorage.setItem(AUTO_SPEAK_KEY, enabled ? 'true' : 'false');
  updateAutoSpeakUI();
}

function updateAutoSpeakUI() {
  const enabled = isAutoSpeakEnabled();
  if (autoSpeakToggleBtn) {
    if (enabled) {
      autoSpeakToggleBtn.classList.add('active');
    } else {
      autoSpeakToggleBtn.classList.remove('active');
    }
  }
  if (autoSpeakBadge) {
    autoSpeakBadge.className = `toolbar-badge ${enabled ? 'on' : 'off'}`;
    autoSpeakBadge.textContent = enabled ? 'ON' : 'OFF';
  }
}

function isWebSearchEnabled() {
  return localStorage.getItem(WEB_SEARCH_KEY) === 'true';
}

function setWebSearchEnabled(enabled) {
  localStorage.setItem(WEB_SEARCH_KEY, enabled ? 'true' : 'false');
  updateWebSearchUI();
}

function updateWebSearchUI() {
  const enabled = isWebSearchEnabled();
  if (webSearchToggleBtn) {
    if (enabled) {
      webSearchToggleBtn.classList.add('active');
    } else {
      webSearchToggleBtn.classList.remove('active');
    }
  }
  if (webSearchBadge) {
    webSearchBadge.className = `toolbar-badge ${enabled ? 'on' : 'off'}`;
    webSearchBadge.textContent = enabled ? 'ON' : 'OFF';
  }
}

function addMessage(role, text) {
  const message = document.createElement('article');
  message.className = `message ${role}`;

  let actionsHtml = '';
  if (role === 'user') {
    actionsHtml = `
      <div class="message-actions">
        <div class="action-btn-wrapper">
          <button class="action-btn copy-btn" type="button" aria-label="複製提示詞">
            ${COPY_ICON_SVG}
          </button>
          <span class="action-tooltip">複製</span>
        </div>
        <div class="action-btn-wrapper">
          <button class="action-btn edit-btn" type="button" aria-label="編輯提示詞">
            ${EDIT_ICON_SVG}
          </button>
          <span class="action-tooltip">編輯提示詞</span>
        </div>
      </div>
    `;
  } else if (role === 'assistant') {
    actionsHtml = `
      <div class="message-actions">
        <div class="action-btn-wrapper">
          <button class="action-btn speak-btn" type="button" aria-label="朗讀回覆">
            ${SPEAKER_ICON_SVG}
          </button>
          <span class="action-tooltip">朗讀回覆</span>
        </div>
        <div class="action-btn-wrapper">
          <button class="action-btn copy-btn" type="button" aria-label="複製回覆">
            ${COPY_ICON_SVG}
          </button>
          <span class="action-tooltip">複製</span>
        </div>
      </div>
    `;
  }

  let roleLabel = 'ERROR';
  if (role === 'user') {
    roleLabel = 'YOU <span class="tag-source client" title="由前端瀏覽器本地送出">💻 前端客戶端</span>';
  } else if (role === 'assistant') {
    roleLabel = 'GEMINI 3.6 FLASH <span class="tag-source server" title="由 Python 後端伺服器調用 Google Gemini API 生成">⚡ 後端 AI 運算</span>';
  }

  message.innerHTML = `
    <div class="message-header">
      <div class="message-meta">${roleLabel}</div>
      ${actionsHtml}
    </div>
    <div class="message-body"></div>
    ${role === 'user' ? `
      <div class="message-edit-box" style="display: none;">
        <textarea class="edit-textarea" rows="3" placeholder="編輯提示詞..."></textarea>
        <div class="edit-actions">
          <button type="button" class="btn-cancel">取消</button>
          <button type="button" class="btn-save">儲存並送出</button>
        </div>
      </div>
    ` : ''}
  `;

  const bodyEl = message.querySelector('.message-body');
  bodyEl.textContent = text;

  // 複製按鈕
  const copyBtn = message.querySelector('.copy-btn');
  if (copyBtn) {
    const tooltip = copyBtn.closest('.action-btn-wrapper').querySelector('.action-tooltip');
    copyBtn.addEventListener('click', () => {
      copyText(bodyEl.textContent, tooltip);
    });
  }

  // 語音朗讀按鈕
  const speakBtn = message.querySelector('.speak-btn');
  if (speakBtn) {
    const tooltip = speakBtn.closest('.action-btn-wrapper').querySelector('.action-tooltip');
    speakBtn.addEventListener('click', () => {
      voiceSynthesisController.toggle(bodyEl.textContent, speakBtn, tooltip);
    });
  }

  // 編輯提示詞
  if (role === 'user') {
    const editBtn = message.querySelector('.edit-btn');
    const editBox = message.querySelector('.message-edit-box');
    const editTextarea = editBox.querySelector('.edit-textarea');
    const cancelBtn = editBox.querySelector('.btn-cancel');
    const saveBtn = editBox.querySelector('.btn-save');

    function autoResize() {
      editTextarea.style.height = 'auto';
      editTextarea.style.height = Math.max(72, editTextarea.scrollHeight) + 'px';
    }

    function enterEdit() {
      message.classList.add('is-editing');
      bodyEl.style.display = 'none';
      editBox.style.display = 'block';
      editTextarea.value = bodyEl.textContent;
      autoResize();
      editTextarea.focus();
    }

    function exitEdit() {
      message.classList.remove('is-editing');
      editBox.style.display = 'none';
      bodyEl.style.display = '';
    }

    editBtn.addEventListener('click', () => {
      if (sendButton.disabled) return;
      enterEdit();
    });

    cancelBtn.addEventListener('click', exitEdit);

    async function handleSave() {
      const newPrompt = editTextarea.value.trim();
      if (!newPrompt || sendButton.disabled) return;

      const oldPrompt = bodyEl.textContent;
      if (newPrompt === oldPrompt) {
        exitEdit();
        return;
      }

      bodyEl.textContent = newPrompt;
      exitEdit();

      if (message.pairedResponse) {
        const respBody = message.pairedResponse.querySelector('.message-body');
        message.pairedResponse.className = 'message assistant';
        respBody.textContent = '思考中...';
        setLoading(true);

        try {
          const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: newPrompt, web_search: isWebSearchEnabled() })
          });
          const data = await response.json();
          if (!response.ok) throw new Error(data.error || '發生未知錯誤');
          respBody.textContent = data.response;
          updateSessionMessage(oldPrompt, newPrompt, data.response);

          if (isAutoSpeakEnabled() && voiceSynthesisController) {
            const spBtn = message.pairedResponse.querySelector('.speak-btn');
            const spTip = spBtn ? spBtn.closest('.action-btn-wrapper').querySelector('.action-tooltip') : null;
            voiceSynthesisController.play(data.response, spBtn, spTip);
          }
        } catch (error) {
          message.pairedResponse.className = 'message error';
          respBody.textContent = error.message;
        } finally {
          setLoading(false);
        }
      } else {
        submitPrompt(newPrompt);
      }
    }

    saveBtn.addEventListener('click', handleSave);

    editTextarea.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        exitEdit();
      } else if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSave();
      }
    });

    editTextarea.addEventListener('input', autoResize);
  }

  messages.appendChild(message);
  messages.scrollTop = messages.scrollHeight;
  return message;
}

function setLoading(isLoading) {
  sendButton.disabled = isLoading;
  sendButton.querySelector('span').textContent = isLoading ? '思考中' : '送出';
}

async function submitPrompt(prompt) {
  if (voiceInputController && voiceInputController.isListening) {
    voiceInputController.stop();
  }

  if (typeof collabController !== 'undefined' && collabController && collabController.isInRoom()) {
    collabController.sendMessage(prompt, isWebSearchEnabled());
    return;
  }

  const userMessage = addMessage('user', prompt);
  appendMessageToCurrentSession('user', prompt);
  setLoading(true);

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, web_search: isWebSearchEnabled() })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || '發生未知錯誤');
    const assistantMessage = addMessage('assistant', data.response);
    userMessage.pairedResponse = assistantMessage;
    appendMessageToCurrentSession('assistant', data.response);

    // 自動朗讀功能：若使用者開啟「自動朗讀」，在收到回覆後自動發聲
    if (isAutoSpeakEnabled() && voiceSynthesisController) {
      const spBtn = assistantMessage.querySelector('.speak-btn');
      const spTip = spBtn ? spBtn.closest('.action-btn-wrapper').querySelector('.action-tooltip') : null;
      voiceSynthesisController.play(data.response, spBtn, spTip);
    }
  } catch (error) {
    const errorMessage = addMessage('error', error.message);
    userMessage.pairedResponse = errorMessage;
    appendMessageToCurrentSession('error', error.message);
  } finally {
    setLoading(false);
  }
}

// 送出表單監聽
if (form) {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const prompt = input.value.trim();
    if (!prompt || sendButton.disabled) return;
    input.value = '';
    submitPrompt(prompt);
  });
}

if (input) {
  input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      form.requestSubmit();
    }
  });
}

// 初始化
updateAuthUI();
updateAutoSpeakUI();
updateWebSearchUI();
renderHistoryList();

// 語音輸入按鈕監聽
if (voiceInputBtn) {
  voiceInputBtn.addEventListener('click', () => {
    voiceInputController.toggle();
  });
}

// 自動朗讀切換按鈕監聽
if (autoSpeakToggleBtn) {
  autoSpeakToggleBtn.addEventListener('click', () => {
    const nextState = !isAutoSpeakEnabled();
    setAutoSpeakEnabled(nextState);
    if (!nextState && voiceSynthesisController) {
      voiceSynthesisController.stop();
    }
  });
}

// 聯網搜尋切換按鈕監聽
if (webSearchToggleBtn) {
  webSearchToggleBtn.addEventListener('click', () => {
    const nextState = !isWebSearchEnabled();
    setWebSearchEnabled(nextState);
  });
}

// 手機聯動中心 Modal 控制
const openPhoneHubBtn = document.querySelector('#openPhoneHubBtn');
const phoneHubModal = document.querySelector('#phoneHubModal');
const closePhoneHubModal = document.querySelector('#closePhoneHubModal');

if (openPhoneHubBtn && phoneHubModal) {
  openPhoneHubBtn.addEventListener('click', () => {
    phoneHubModal.style.display = 'flex';
  });
}

if (closePhoneHubModal && phoneHubModal) {
  closePhoneHubModal.addEventListener('click', () => {
    phoneHubModal.style.display = 'none';
  });
}

if (phoneHubModal) {
  phoneHubModal.addEventListener('click', (e) => {
    if (e.target === phoneHubModal) {
      phoneHubModal.style.display = 'none';
    }
  });
}

// Phone Hub 標籤分頁切換
const hubTabs = document.querySelectorAll('.hub-tab');
if (hubTabs.length > 0) {
  hubTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      hubTabs.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.hub-tab-content').forEach(c => {
        c.classList.remove('active');
        c.style.display = 'none';
      });
      tab.classList.add('active');
      const targetId = tab.getAttribute('data-tab');
      const targetContent = document.getElementById(targetId);
      if (targetContent) {
        targetContent.classList.add('active');
        targetContent.style.display = 'block';
      }
    });
  });
}

// 手機原生鬧鐘 Intent
const alarmTimeInput = document.querySelector('#alarmTimeInput');
const alarmLabelInput = document.querySelector('#alarmLabelInput');
const startAndroidAlarmLink = document.querySelector('#startAndroidAlarmLink');

function updateAndroidAlarmIntent() {
  if (!startAndroidAlarmLink) return;
  const timeVal = alarmTimeInput ? alarmTimeInput.value : '07:30';
  const labelVal = alarmLabelInput ? alarmLabelInput.value.trim() : '早起衝刺';
  const [hours, minutes] = (timeVal || '07:30').split(':').map(n => parseInt(n, 10));
  const intentUri = `intent:#Intent;action=android.intent.action.SET_ALARM;i.android.intent.extra.alarm.HOUR=${hours};i.android.intent.extra.alarm.MINUTES=${minutes};S.android.intent.extra.alarm.MESSAGE=${encodeURIComponent(labelVal)};B.android.intent.extra.alarm.SKIP_UI=false;end`;
  startAndroidAlarmLink.href = intentUri;
}

if (alarmTimeInput) alarmTimeInput.addEventListener('input', updateAndroidAlarmIntent);
if (alarmLabelInput) alarmLabelInput.addEventListener('input', updateAndroidAlarmIntent);
updateAndroidAlarmIntent();

// ==========================================
// 6. 手機掃碼同步功能
// ==========================================
const syncButton = document.getElementById('syncButton');
const syncModal = document.getElementById('syncModal');
const closeSyncModal = document.getElementById('closeSyncModal');
const qrCodeImg = document.getElementById('qrCodeImg');
const qrCodeUrlText = document.getElementById('qrCodeUrlText');
const copyUrlBtn = document.getElementById('copyUrlBtn');

if (syncButton && syncModal) {
  syncButton.addEventListener('click', () => {
    const currentUrl = window.location.href;
    if (qrCodeUrlText) qrCodeUrlText.textContent = currentUrl;
    if (qrCodeImg) {
      qrCodeImg.src = 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&margin=4&data=' + encodeURIComponent(currentUrl);
    }
    syncModal.style.display = 'flex';
  });

  if (closeSyncModal) {
    closeSyncModal.addEventListener('click', () => {
      syncModal.style.display = 'none';
    });
  }

  syncModal.addEventListener('click', (e) => {
    if (e.target === syncModal) {
      syncModal.style.display = 'none';
    }
  });

  if (copyUrlBtn) {
    copyUrlBtn.addEventListener('click', () => {
      const url = window.location.href;
      copyText(url, null);
      const originalText = copyUrlBtn.innerHTML;
      copyUrlBtn.innerHTML = '<span>✅ 已複製公開網址！</span>';
      setTimeout(() => {
        copyUrlBtn.innerHTML = originalText;
      }, 1800);
    });
  }
}

// ==========================================
// 7. 右下角待辦事項小工具與「問 AI」互動邏輯
// ==========================================
const todoWidget = document.getElementById('todoWidget');
const todoToggleBtn = document.getElementById('todoToggleBtn');
const todoCard = document.getElementById('todoCard');
const todoMinimizeBtn = document.getElementById('todoMinimizeBtn');
const todoAddForm = document.getElementById('todoAddForm');
const todoInput = document.getElementById('todoInput');
const todoList = document.getElementById('todoList');
const todoCountBadge = document.getElementById('todoCountBadge');
const todoToggleBadge = document.getElementById('todoToggleBadge');

const TODO_STORAGE_KEY = 'gura_todo_items';

// 預設示範事項
const DEFAULT_TODOS = [
  { id: 'todo_1', text: '整理本週重要代辦清單', completed: false },
  { id: 'todo_2', text: '準備英語口說發表題目大綱', completed: false },
  { id: 'todo_3', text: '請 Gura 推薦高效率時間管理法', completed: false }
];

function loadTodos() {
  try {
    const raw = localStorage.getItem(TODO_STORAGE_KEY);
    if (raw) {
      return JSON.parse(raw);
    }
  } catch (e) {
    console.error('Failed to parse todos from localStorage:', e);
  }
  return DEFAULT_TODOS;
}

let todoItems = loadTodos();

function saveTodos() {
  try {
    localStorage.setItem(TODO_STORAGE_KEY, JSON.stringify(todoItems));
  } catch (e) {
    console.error('Failed to save todos:', e);
  }
}

function updateTodoBadges() {
  const activeCount = todoItems.filter(item => !item.completed).length;
  if (todoCountBadge) todoCountBadge.textContent = activeCount;
  if (todoToggleBadge) todoToggleBadge.textContent = activeCount;
}

function renderTodoList() {
  if (!todoList) return;
  todoList.innerHTML = '';

  if (todoItems.length === 0) {
    todoList.innerHTML = '<div class="todo-empty">暫無待辦事項<br>在上方輸入框新增一項吧！</div>';
    updateTodoBadges();
    return;
  }

  todoItems.forEach((item, index) => {
    const row = document.createElement('div');
    row.className = `todo-item ${item.completed ? 'completed' : ''}`;
    row.dataset.id = item.id;

    // 勾選框
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'todo-checkbox';
    checkbox.checked = !!item.completed;
    checkbox.title = item.completed ? '標記為未完成' : '標記為完成';
    checkbox.addEventListener('change', () => {
      item.completed = checkbox.checked;
      saveTodos();
      renderTodoList();
    });

    // 事項文字 (點擊也可以問 AI)
    const textSpan = document.createElement('span');
    textSpan.className = 'todo-text';
    textSpan.textContent = item.text;
    textSpan.title = '點擊向 AI 詢問此事項';
    textSpan.addEventListener('click', () => {
      askAiAboutTodo(item.text);
    });

    // 「✨ 問 AI」專用按鈕
    const askAiBtn = document.createElement('button');
    askAiBtn.type = 'button';
    askAiBtn.className = 'todo-ask-ai-btn';
    askAiBtn.title = '請 Gura 針對此待辦事項提供執行規劃與建議';
    askAiBtn.innerHTML = '<span>✨ 問 AI</span>';
    askAiBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      askAiAboutTodo(item.text);
    });

    // 刪除按鈕
    const delBtn = document.createElement('button');
    delBtn.type = 'button';
    delBtn.className = 'todo-del-btn';
    delBtn.title = '刪除此事項';
    delBtn.textContent = '✕';
    delBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      todoItems.splice(index, 1);
      saveTodos();
      renderTodoList();
    });

    row.appendChild(checkbox);
    row.appendChild(textSpan);
    row.appendChild(askAiBtn);
    row.appendChild(delBtn);

    todoList.appendChild(row);
  });

  updateTodoBadges();
}

// 核心功能：點擊事項向 AI 發問
function askAiAboutTodo(taskText) {
  if (!taskText) return;
  const prompt = `請針對以下待辦事項提供具體執行步驟、規劃建議與輔助方案：【${taskText}】`;

  // 填入輸入框並提交
  if (input) {
    input.value = prompt;
    input.focus();
  }

  // 自動送出查詢
  submitPrompt(prompt);

  // 在手機版上點擊問 AI 時，自動收合卡片以方便觀看對話
  if (window.innerWidth <= 768) {
    if (todoCard) todoCard.style.display = 'none';
    if (todoToggleBtn) todoToggleBtn.style.display = 'inline-flex';
  }
}

// 新增待辦事項監聽
if (todoAddForm && todoInput) {
  todoAddForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = todoInput.value.trim();
    if (!text) return;

    const newItem = {
      id: 'todo_' + Date.now(),
      text: text,
      completed: false
    };

    todoItems.unshift(newItem);
    saveTodos();
    renderTodoList();

    todoInput.value = '';
    todoInput.focus();
  });
}

// 開啟 / 收合待辦小工具
if (todoToggleBtn && todoCard) {
  todoToggleBtn.addEventListener('click', () => {
    todoCard.style.display = 'flex';
    todoToggleBtn.style.display = 'none';
    if (todoInput) todoInput.focus();
  });
}

if (todoMinimizeBtn && todoCard && todoToggleBtn) {
  todoMinimizeBtn.addEventListener('click', () => {
    todoCard.style.display = 'none';
    todoToggleBtn.style.display = 'inline-flex';
  });
}

// 初始化渲染待辦清單
renderTodoList();

// ==========================================
// 8. Gemini 風格側邊欄互動 (折疊、筆記本、搜尋聚焦)
// ==========================================
const mainSidebar = document.querySelector('#mainSidebar');
const sidebarCollapseBtn = document.querySelector('#sidebarCollapseBtn');
const mobileMenuBtn = document.querySelector('#mobileMenuBtn');
const sidebarBackdrop = document.querySelector('#sidebarBackdrop');
const mobileSidebarCloseBtn = document.querySelector('#mobileSidebarCloseBtn');
const searchChatToggleBtn = document.querySelector('#searchChatToggleBtn');
const mediaLibraryBtn = document.querySelector('#mediaLibraryBtn');
const addNotebookBtn = document.querySelector('#addNotebookBtn');
const notebooksList = document.querySelector('#notebooksList');
const allNotebooksBtn = document.querySelector('#allNotebooksBtn');
const sidebarUserProfile = document.querySelector('#sidebarUserProfile');
const sidebarSettingsBtn = document.querySelector('#sidebarSettingsBtn');

function openMobileSidebar() {
  if (mainSidebar) {
    mainSidebar.classList.add('mobile-open');
  }
  if (sidebarBackdrop) {
    sidebarBackdrop.style.display = 'block';
  }
  document.body.classList.add('sidebar-open-locked');
}

function closeMobileSidebar() {
  if (mainSidebar) {
    mainSidebar.classList.remove('mobile-open');
  }
  if (sidebarBackdrop) {
    sidebarBackdrop.style.display = 'none';
  }
  document.body.classList.remove('sidebar-open-locked');
}

if (mobileMenuBtn) {
  mobileMenuBtn.addEventListener('click', () => {
    if (mainSidebar && mainSidebar.classList.contains('mobile-open')) {
      closeMobileSidebar();
    } else {
      openMobileSidebar();
    }
  });
}

if (sidebarBackdrop) {
  sidebarBackdrop.addEventListener('click', closeMobileSidebar);
}

if (mobileSidebarCloseBtn) {
  mobileSidebarCloseBtn.addEventListener('click', closeMobileSidebar);
}

if (sidebarCollapseBtn && mainSidebar) {
  sidebarCollapseBtn.addEventListener('click', () => {
    if (window.innerWidth <= 768) {
      closeMobileSidebar();
    } else {
      mainSidebar.classList.toggle('collapsed');
      sidebarCollapseBtn.title = mainSidebar.classList.contains('collapsed') ? '展開側邊欄' : '收合側邊欄';
    }
  });
}

if (mediaLibraryBtn) {
  mediaLibraryBtn.addEventListener('click', () => {
    alert('媒體庫已為您就緒！您可以存放常用提示詞、對話靈感與附件檔案。');
  });
}

if (sidebarUserProfile) {
  sidebarUserProfile.addEventListener('click', openLoginModal);
}

if (sidebarSettingsBtn) {
  sidebarSettingsBtn.addEventListener('click', openLoginModal);
}

// ==========================================
// 9. 多人專案連機協作控制器 (CollabController)
// ==========================================
class CollabController {
  constructor() {
    this.roomId = null;
    this.userId = localStorage.getItem(COLLAB_USER_ID_KEY) || ('u_' + Math.random().toString(36).substring(2, 9));
    localStorage.setItem(COLLAB_USER_ID_KEY, this.userId);
    this.userName = localStorage.getItem(COLLAB_NICKNAME_KEY) || (getUser() ? getUser().name : '組員');
    this.pollTimer = null;
    this.lastMessageId = 0;
    this.renderedMessageIds = new Set();
    this.roomData = null;
    this.isSyncing = false;
  }

  isInRoom() {
    return Boolean(this.roomId);
  }

  init() {
    this.bindEvents();

    const savedNick = localStorage.getItem(COLLAB_NICKNAME_KEY) || (getUser() ? getUser().name : '');
    if (savedNick) {
      if (collabCreateNicknameInput) collabCreateNicknameInput.value = savedNick;
      if (collabJoinNicknameInput) collabJoinNicknameInput.value = savedNick;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const roomParam = urlParams.get('room');
    if (roomParam) {
      this.openModal('join', roomParam.toUpperCase());
      return;
    }

    const savedRoomId = localStorage.getItem(COLLAB_ROOM_KEY);
    if (savedRoomId) {
      this.reconnect(savedRoomId);
    }
  }

  bindEvents() {
    if (collabButton) {
      collabButton.addEventListener('click', () => this.handleOpenCollab());
    }
    if (sidebarCollabBtn) {
      sidebarCollabBtn.addEventListener('click', () => this.handleOpenCollab());
    }

    if (closeCollabModal) {
      closeCollabModal.addEventListener('click', () => this.closeModal());
    }
    if (collabModal) {
      collabModal.addEventListener('click', (e) => {
        if (e.target === collabModal) this.closeModal();
      });
    }

    if (collabTabCreateBtn && collabTabJoinBtn) {
      collabTabCreateBtn.addEventListener('click', () => this.switchTab('create'));
      collabTabJoinBtn.addEventListener('click', () => this.switchTab('join'));
    }

    if (startCollabCreateBtn) {
      startCollabCreateBtn.addEventListener('click', () => this.handleCreate());
    }

    if (startCollabJoinBtn) {
      startCollabJoinBtn.addEventListener('click', () => this.handleJoin());
    }

    if (collabInviteBtn) {
      collabInviteBtn.addEventListener('click', () => this.openModal('active'));
    }
    if (collabNotesBtn) {
      collabNotesBtn.addEventListener('click', () => {
        this.openModal('active');
        if (collabSharedNotesInput) {
          setTimeout(() => collabSharedNotesInput.focus(), 200);
        }
      });
    }
    if (collabLeaveBtn) {
      collabLeaveBtn.addEventListener('click', () => this.leaveRoom(true));
    }
    if (exitCollabRoomBtn) {
      exitCollabRoomBtn.addEventListener('click', () => this.leaveRoom(true));
    }

    if (copyCollabCodeBtn) {
      copyCollabCodeBtn.addEventListener('click', () => {
        if (this.roomId) {
          copyText(this.roomId, null);
          const orig = copyCollabCodeBtn.textContent;
          copyCollabCodeBtn.textContent = '已複製';
          setTimeout(() => { copyCollabCodeBtn.textContent = orig; }, 1500);
        }
      });
    }
    if (collabBannerRoomCode) {
      collabBannerRoomCode.addEventListener('click', () => {
        if (this.roomId) {
          copyText(this.roomId, null);
          alert(`已複製連機代碼：${this.roomId}`);
        }
      });
    }
    if (copyCollabUrlBtn) {
      copyCollabUrlBtn.addEventListener('click', () => {
        if (collabActiveShareUrl && collabActiveShareUrl.value) {
          copyText(collabActiveShareUrl.value, null);
          const orig = copyCollabUrlBtn.innerHTML;
          copyCollabUrlBtn.innerHTML = '✅ 已複製連結';
          setTimeout(() => { copyCollabUrlBtn.innerHTML = orig; }, 1800);
        }
      });
    }

    if (saveCollabNotesBtn) {
      saveCollabNotesBtn.addEventListener('click', () => this.saveNotes());
    }
  }

  handleOpenCollab() {
    if (this.isInRoom()) {
      this.openModal('active');
    } else {
      this.openModal('create');
    }
  }

  openModal(view = 'create', prefillCode = '') {
    if (!collabModal) return;
    collabModal.style.display = 'flex';

    if (view === 'active' && this.isInRoom()) {
      if (collabEntryView) collabEntryView.style.display = 'none';
      if (collabActiveView) collabActiveView.style.display = 'block';
    } else {
      if (collabEntryView) collabEntryView.style.display = 'block';
      if (collabActiveView) collabActiveView.style.display = 'none';
      if (view === 'join') {
        this.switchTab('join');
        if (prefillCode && collabJoinCodeInput) {
          collabJoinCodeInput.value = prefillCode;
        }
      } else {
        this.switchTab('create');
      }
    }
  }

  closeModal() {
    if (collabModal) collabModal.style.display = 'none';
  }

  switchTab(tab) {
    if (tab === 'create') {
      if (collabTabCreateBtn) collabTabCreateBtn.classList.add('active');
      if (collabTabJoinBtn) collabTabJoinBtn.classList.remove('active');
      if (collabCreateTab) collabCreateTab.style.display = 'flex';
      if (collabJoinTab) collabJoinTab.style.display = 'none';
    } else {
      if (collabTabJoinBtn) collabTabJoinBtn.classList.add('active');
      if (collabTabCreateBtn) collabTabCreateBtn.classList.remove('active');
      if (collabJoinTab) collabJoinTab.style.display = 'flex';
      if (collabCreateTab) collabCreateTab.style.display = 'none';
    }
  }

  async handleCreate() {
    const projectName = collabCreateNameInput ? collabCreateNameInput.value.trim() : '';
    const projectGoal = collabCreateGoalInput ? collabCreateGoalInput.value.trim() : '';
    const nickname = collabCreateNicknameInput ? collabCreateNicknameInput.value.trim() : '';

    if (!projectName) {
      alert('請填寫專案名稱！');
      return;
    }
    if (!nickname) {
      alert('請填寫您的暱稱！');
      return;
    }

    this.userName = nickname;
    localStorage.setItem(COLLAB_NICKNAME_KEY, nickname);

    try {
      if (startCollabCreateBtn) startCollabCreateBtn.disabled = true;
      const res = await fetch('/api/collab/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_name: projectName,
          project_goal: projectGoal,
          creator_name: nickname,
          user_id: this.userId
        })
      });
      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data.error || '建立連機專案失敗');
      }

      this.enterRoom(data.room);
      this.closeModal();
    } catch (err) {
      alert('建立專案連機失敗：' + err.message);
    } finally {
      if (startCollabCreateBtn) startCollabCreateBtn.disabled = false;
    }
  }

  async handleJoin() {
    const code = collabJoinCodeInput ? collabJoinCodeInput.value.trim() : '';
    const nickname = collabJoinNicknameInput ? collabJoinNicknameInput.value.trim() : '';

    if (!code) {
      alert('請輸入房間代碼或貼上邀請連結！');
      return;
    }
    if (!nickname) {
      alert('請填寫您的暱稱！');
      return;
    }

    this.userName = nickname;
    localStorage.setItem(COLLAB_NICKNAME_KEY, nickname);

    try {
      if (startCollabJoinBtn) startCollabJoinBtn.disabled = true;
      const res = await fetch('/api/collab/join', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          room_id: code,
          user_name: nickname,
          user_id: this.userId
        })
      });
      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data.error || '加入房間失敗，請確認代碼是否正確。');
      }

      this.enterRoom(data.room);
      this.closeModal();
    } catch (err) {
      alert('加入連機房間失敗：' + err.message);
    } finally {
      if (startCollabJoinBtn) startCollabJoinBtn.disabled = false;
    }
  }

  async reconnect(roomId) {
    try {
      const res = await fetch(`/api/collab/sync/${roomId}?since=0&user_id=${this.userId}&user_name=${encodeURIComponent(this.userName)}`);
      const data = await res.json();
      if (res.ok && data.success) {
        this.enterRoom({
          room_id: data.room_id,
          project_name: data.project_name,
          project_goal: data.project_goal,
          creator_id: data.creator_id,
          members: data.members.reduce((acc, m) => { acc[m.user_id] = m; return acc; }, {}),
          messages: data.new_messages,
          shared_notes: data.shared_notes
        });
      } else {
        localStorage.removeItem(COLLAB_ROOM_KEY);
      }
    } catch (e) {
      console.warn('無法恢復連機房間：', e);
    }
  }

  enterRoom(room) {
    this.roomId = room.room_id;
    this.roomData = room;
    localStorage.setItem(COLLAB_ROOM_KEY, this.roomId);

    if (collabButton) {
      collabButton.classList.add('in-room');
    }
    if (collabButtonText) {
      collabButtonText.textContent = room.project_name || '連機中';
    }
    if (collabStatusDot) {
      collabStatusDot.style.display = 'inline-block';
    }
    if (sidebarCollabCountBadge) {
      sidebarCollabCountBadge.style.display = 'inline-flex';
    }

    if (collabBanner) {
      collabBanner.style.display = 'flex';
    }
    if (collabBannerProjectName) {
      collabBannerProjectName.textContent = room.project_name;
    }
    if (collabBannerRoomCode) {
      collabBannerRoomCode.textContent = room.room_id;
    }

    if (collabActiveProjectTitle) collabActiveProjectTitle.textContent = room.project_name;
    if (collabActiveProjectGoal) collabActiveProjectGoal.textContent = room.project_goal || '無專案目標';
    if (collabActiveRoomCode) collabActiveRoomCode.textContent = room.room_id;

    const inviteUrl = `${window.location.origin}${window.location.pathname}?room=${room.room_id}`;
    if (collabActiveShareUrl) collabActiveShareUrl.value = inviteUrl;
    if (collabQrImg) {
      collabQrImg.src = 'https://api.qrserver.com/v1/create-qr-code/?size=180x180&margin=4&data=' + encodeURIComponent(inviteUrl);
    }
    if (collabSharedNotesInput) {
      collabSharedNotesInput.value = room.shared_notes || '';
    }

    if (messages) messages.innerHTML = '';
    this.renderedMessageIds.clear();
    this.lastMessageId = 0;

    if (Array.isArray(room.messages)) {
      room.messages.forEach(msg => this.renderMessage(msg));
      if (room.messages.length > 0) {
        this.lastMessageId = room.messages[room.messages.length - 1].id;
      }
    }

    const membersList = Array.isArray(room.members) ? room.members : Object.values(room.members || {});
    this.updateMembers(membersList);

    this.startPolling();
  }

  updateMembers(membersList) {
    if (!Array.isArray(membersList)) return;
    const count = membersList.length;

    if (sidebarCollabCountBadge) {
      sidebarCollabCountBadge.textContent = count;
      sidebarCollabCountBadge.style.display = 'inline-flex';
    }

    if (collabMemberCountText) {
      collabMemberCountText.textContent = `${count}人連線`;
    }
    if (collabAvatarStack) {
      collabAvatarStack.innerHTML = '';
      membersList.slice(0, 4).forEach(m => {
        const av = document.createElement('div');
        av.className = 'collab-stack-avatar';
        av.style.backgroundColor = m.color || '#0284c7';
        av.textContent = (m.user_name || 'U').slice(0, 1).toUpperCase();
        av.title = `${m.user_name}${m.is_host ? ' (主揪人)' : ''}`;
        collabAvatarStack.appendChild(av);
      });
      if (count > 4) {
        const extra = document.createElement('div');
        extra.className = 'collab-stack-avatar';
        extra.style.backgroundColor = '#64748b';
        extra.textContent = `+${count - 4}`;
        collabAvatarStack.appendChild(extra);
      }
    }

    if (collabActiveMemberCount) {
      collabActiveMemberCount.textContent = count;
    }
    if (collabActiveMemberList) {
      collabActiveMemberList.innerHTML = '';
      membersList.forEach(m => {
        const chip = document.createElement('div');
        chip.className = 'collab-member-chip';
        chip.innerHTML = `
          <div class="collab-chip-avatar" style="background-color: ${m.color || '#0284c7'};">${(m.user_name || 'U').slice(0, 1).toUpperCase()}</div>
          <span>${m.user_name}</span>
          ${m.is_host ? '<span class="collab-chip-host-badge">主揪人</span>' : ''}
          ${m.user_id === this.userId ? '<span style="font-size: 10px; color: #64748b;">(你)</span>' : ''}
        `;
        collabActiveMemberList.appendChild(chip);
      });
    }
  }

  renderMessage(msg) {
    if (this.renderedMessageIds.has(msg.id)) return;
    this.renderedMessageIds.add(msg.id);

    if (msg.role === 'system') {
      const sysEl = document.createElement('article');
      sysEl.className = 'message system';
      sysEl.innerHTML = `<div class="collab-system-pill">${msg.text}</div>`;
      messages.appendChild(sysEl);
      messages.scrollTop = messages.scrollHeight;
      return sysEl;
    }

    const message = document.createElement('article');
    const isSelf = msg.user_id === this.userId;
    const isAi = msg.is_ai || msg.role === 'assistant';

    message.className = `message ${isAi ? 'assistant' : 'user'} ${isSelf ? 'is-self' : ''}`;

    let actionsHtml = '';
    if (isAi) {
      actionsHtml = `
        <div class="message-actions">
          <div class="action-btn-wrapper">
            <button class="action-btn speak-btn" type="button" aria-label="朗讀回覆">
              ${SPEAKER_ICON_SVG}
            </button>
            <span class="action-tooltip">朗讀回覆</span>
          </div>
          <div class="action-btn-wrapper">
            <button class="action-btn copy-btn" type="button" aria-label="複製回覆">
              ${COPY_ICON_SVG}
            </button>
            <span class="action-tooltip">複製</span>
          </div>
        </div>
      `;
    } else {
      actionsHtml = `
        <div class="message-actions">
          <div class="action-btn-wrapper">
            <button class="action-btn copy-btn" type="button" aria-label="複製訊息">
              ${COPY_ICON_SVG}
            </button>
            <span class="action-tooltip">複製</span>
          </div>
        </div>
      `;
    }

    let authorHtml = '';
    if (isAi) {
      authorHtml = `
        <div class="message-collab-author">
          <div class="collab-author-avatar" style="background-color: #7c3aed;">AI</div>
          <span class="collab-author-name">Gemini 3.6 Flash</span>
          <span class="collab-role-tag ai" title="由 Python 後端伺服器調用 Google Gemini API">⚡ 後端 AI 運算</span>
        </div>
      `;
    } else {
      const initial = (msg.user_name || 'U').slice(0, 1).toUpperCase();
      const color = msg.color || '#0284c7';
      authorHtml = `
        <div class="message-collab-author">
          <div class="collab-author-avatar" style="background-color: ${color};">${initial}</div>
          <span class="collab-author-name">${msg.user_name || '組員'}</span>
          ${isSelf ? '<span class="collab-role-tag member" title="由您本地前端送出">💻 前端 (你)</span>' : '<span class="collab-role-tag member">💻 前端組員</span>'}
        </div>
      `;
    }

    message.innerHTML = `
      <div class="message-header">
        ${authorHtml}
        ${actionsHtml}
      </div>
      <div class="message-body"></div>
    `;

    const bodyEl = message.querySelector('.message-body');
    bodyEl.textContent = msg.text;

    if (isAi && Array.isArray(msg.search_sources) && msg.search_sources.length > 0) {
      const sourcesBox = document.createElement('div');
      sourcesBox.className = 'search-sources-box';
      sourcesBox.innerHTML = `
        <div class="search-sources-title">
          <span>🌐 聯網搜尋參考來源：</span>
        </div>
        <div class="search-sources-list">
          ${msg.search_sources.map(s => `
            <a class="search-source-chip" href="${s.uri}" target="_blank" rel="noopener noreferrer" title="${s.title}">
              <span>🔗 ${s.title || s.uri}</span>
            </a>
          `).join('')}
        </div>
      `;
      message.appendChild(sourcesBox);
    }

    const copyBtn = message.querySelector('.copy-btn');
    if (copyBtn) {
      const tooltip = copyBtn.closest('.action-btn-wrapper').querySelector('.action-tooltip');
      copyBtn.addEventListener('click', () => {
        copyText(bodyEl.textContent, tooltip);
      });
    }

    const speakBtn = message.querySelector('.speak-btn');
    if (speakBtn && voiceSynthesisController) {
      const tooltip = speakBtn.closest('.action-btn-wrapper').querySelector('.action-tooltip');
      speakBtn.addEventListener('click', () => {
        voiceSynthesisController.toggle(bodyEl.textContent, speakBtn, tooltip);
      });
    }

    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
    return message;
  }

  startPolling() {
    this.stopPolling();
    this.pollTimer = setInterval(() => this.pollSync(), 1500);
  }

  stopPolling() {
    if (this.pollTimer) {
      clearInterval(this.pollTimer);
      this.pollTimer = null;
    }
  }

  async pollSync() {
    if (!this.roomId || this.isSyncing) return;
    this.isSyncing = true;

    try {
      const res = await fetch(`/api/collab/sync/${this.roomId}?since=${this.lastMessageId}&user_id=${this.userId}&user_name=${encodeURIComponent(this.userName)}`);
      if (res.status === 404) {
        this.stopPolling();
        alert('專案連機房間已關閉或不存在。');
        this.leaveRoom(false);
        return;
      }

      const data = await res.json();
      if (data.success) {
        if (Array.isArray(data.new_messages) && data.new_messages.length > 0) {
          data.new_messages.forEach(msg => {
            this.renderMessage(msg);
          });
          this.lastMessageId = data.latest_message_id;
        }

        if (Array.isArray(data.members)) {
          this.updateMembers(data.members);
        }

        if (collabSharedNotesInput && document.activeElement !== collabSharedNotesInput) {
          if (data.shared_notes !== undefined && collabSharedNotesInput.value !== data.shared_notes) {
            collabSharedNotesInput.value = data.shared_notes;
          }
        }
      }
    } catch (err) {
      console.warn('Collab sync error:', err);
    } finally {
      this.isSyncing = false;
    }
  }

  async sendMessage(prompt, webSearch = false) {
    if (!this.roomId) return;
    setLoading(true);

    try {
      const res = await fetch('/api/collab/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          room_id: this.roomId,
          user_id: this.userId,
          user_name: this.userName,
          text: prompt,
          web_search: webSearch,
          trigger_ai: true
        })
      });
      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data.error || '傳送訊息失敗');
      }

      await this.pollSync();

      if (data.ai_message && isAutoSpeakEnabled() && voiceSynthesisController) {
        const lastAssistant = messages.querySelector('.message.assistant:last-child');
        if (lastAssistant) {
          const spBtn = lastAssistant.querySelector('.speak-btn');
          const spTip = spBtn ? spBtn.closest('.action-btn-wrapper').querySelector('.action-tooltip') : null;
          voiceSynthesisController.play(data.ai_message.text, spBtn, spTip);
        }
      }
    } catch (err) {
      alert('連機發言失敗：' + err.message);
    } finally {
      setLoading(false);
    }
  }

  async saveNotes() {
    if (!this.roomId || !collabSharedNotesInput) return;
    const notes = collabSharedNotesInput.value;
    if (collabNotesStatus) collabNotesStatus.textContent = '同步儲存中...';

    try {
      const res = await fetch('/api/collab/notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          room_id: this.roomId,
          user_id: this.userId,
          notes: notes
        })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        if (collabNotesStatus) {
          collabNotesStatus.textContent = '✅ 已儲存並同步全體';
          setTimeout(() => {
            if (collabNotesStatus) collabNotesStatus.textContent = '已同步';
          }, 2000);
        }
      } else {
        throw new Error(data.error || '儲存失敗');
      }
    } catch (e) {
      if (collabNotesStatus) collabNotesStatus.textContent = '❌ 同步失敗';
      alert('儲存筆記失敗：' + e.message);
    }
  }

  async leaveRoom(confirmFirst = true) {
    if (confirmFirst) {
      if (!confirm('確定要退出目前的專案連機房間嗎？')) return;
    }

    const currentRoom = this.roomId;
    this.stopPolling();
    this.roomId = null;
    this.roomData = null;
    localStorage.removeItem(COLLAB_ROOM_KEY);

    const url = new URL(window.location.href);
    if (url.searchParams.has('room')) {
      url.searchParams.delete('room');
      window.history.replaceState({}, '', url.pathname + (url.search ? url.search : ''));
    }

    if (collabButton) collabButton.classList.remove('in-room');
    if (collabButtonText) collabButtonText.textContent = '專案連機';
    if (collabStatusDot) collabStatusDot.style.display = 'none';
    if (sidebarCollabCountBadge) sidebarCollabCountBadge.style.display = 'none';
    if (collabBanner) collabBanner.style.display = 'none';

    this.closeModal();

    if (currentRoom) {
      fetch('/api/collab/leave', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          room_id: currentRoom,
          user_id: this.userId,
          user_name: this.userName
        })
      }).catch(e => console.warn('通知伺服器退出失敗：', e));
    }

    startNewSession(true);
  }
}

// 實例化並啟動協作控制器
const collabController = new CollabController();
collabController.init();

// ==========================================
// 10. 前後端系統架構與狀態監控控制器 (Architecture & Backend Status)
// ==========================================
const backendStatusBtn = document.querySelector('#backendStatusBtn');
const architectureModal = document.querySelector('#architectureModal');
const closeArchitectureModal = document.querySelector('#closeArchitectureModal');
const archCloseBtn = document.querySelector('#archCloseBtn');
const archRefreshPingBtn = document.querySelector('#archRefreshPingBtn');

const archClientEnv = document.querySelector('#archClientEnv');
const archBackendStatusIndicator = document.querySelector('#archBackendStatusIndicator');
const archBackendRuntime = document.querySelector('#archBackendRuntime');
const archBackendModel = document.querySelector('#archBackendModel');
const archTunnelStatus = document.querySelector('#archTunnelStatus');
const archPingValue = document.querySelector('#archPingValue');
const archUptimeValue = document.querySelector('#archUptimeValue');

async function checkBackendPing() {
  if (archPingValue) archPingValue.textContent = '測速中...';
  const startTime = performance.now();
  try {
    const res = await fetch('/api/system/ping');
    const endTime = performance.now();
    const duration = Math.round(endTime - startTime);
    if (res.ok) {
      if (archPingValue) archPingValue.textContent = `${duration} ms (極速)`;
      return duration;
    }
  } catch (e) {
    if (archPingValue) archPingValue.textContent = '離線 / 連線逾時';
  }
  return null;
}

async function loadBackendSystemStatus() {
  try {
    const res = await fetch('/api/system/status');
    if (!res.ok) throw new Error('無法取得系統資訊');
    const data = await res.json();

    if (archBackendRuntime) archBackendRuntime.textContent = data.backend.runtime + ' · Flask';
    if (archBackendModel) archBackendModel.textContent = data.backend.ai_model || 'Gemini 3.6 Flash';
    if (archUptimeValue) archUptimeValue.textContent = data.backend.uptime_text || '剛剛啟動';
    if (archTunnelStatus) {
      const pubUrl = data.tunnel.public_url;
      archTunnelStatus.textContent = pubUrl.startsWith('http') ? `Cloudflare (已連線)` : '本機模式 (127.0.0.1)';
      archTunnelStatus.title = pubUrl;
    }
    if (archClientEnv) {
      const isMobile = window.innerWidth <= 768;
      archClientEnv.textContent = `${isMobile ? '行動裝置手機端' : '桌面電腦端'} (${navigator.language || 'zh-TW'})`;
    }
    if (archBackendStatusIndicator) {
      archBackendStatusIndicator.textContent = '🟢 服務在線';
      archBackendStatusIndicator.style.color = '#16a34a';
    }
  } catch (err) {
    console.warn('System status fetch failed:', err);
    if (archBackendStatusIndicator) {
      archBackendStatusIndicator.textContent = '🔴 連線異常';
      archBackendStatusIndicator.style.color = '#ef4444';
    }
  }
}

function openArchitectureModal() {
  if (!architectureModal) return;
  architectureModal.style.display = 'flex';
  loadBackendSystemStatus();
  checkBackendPing();
}

function closeArchitectureModalWindow() {
  if (architectureModal) architectureModal.style.display = 'none';
}

if (backendStatusBtn) {
  backendStatusBtn.addEventListener('click', openArchitectureModal);
}
if (closeArchitectureModal) {
  closeArchitectureModal.addEventListener('click', closeArchitectureModalWindow);
}
if (archCloseBtn) {
  archCloseBtn.addEventListener('click', closeArchitectureModalWindow);
}
if (architectureModal) {
  architectureModal.addEventListener('click', (e) => {
    if (e.target === architectureModal) closeArchitectureModalWindow();
  });
}
if (archRefreshPingBtn) {
  archRefreshPingBtn.addEventListener('click', () => {
    checkBackendPing();
    loadBackendSystemStatus();
  });
}

// 定期檢查後端連線狀態 (每 30 秒)
setInterval(async () => {
  try {
    const res = await fetch('/api/system/ping');
    if (backendStatusBtn) {
      const dot = backendStatusBtn.querySelector('.backend-status-indicator');
      const txt = backendStatusBtn.querySelector('.backend-status-text');
      if (dot && txt) {
        dot.style.background = res.ok ? '#10b981' : '#ef4444';
        txt.textContent = res.ok ? '後端在線' : '後端離線';
      }
    }
  } catch (e) {
    if (backendStatusBtn) {
      const dot = backendStatusBtn.querySelector('.backend-status-indicator');
      const txt = backendStatusBtn.querySelector('.backend-status-text');
      if (dot && txt) {
        dot.style.background = '#ef4444';
        txt.textContent = '後端離線';
      }
    }
  }
}, 30000);





