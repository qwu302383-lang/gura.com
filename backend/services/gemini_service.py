import os
import sys

# 確保可以載入根目錄的 ta 模組
from backend.config import PROJECT_ROOT
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ta import (
    GeminiAuthenticationError,
    generate_chat_reply,
    generate_response,
    search_web_snippets,
    API_KEY,
    MODEL,
)

__all__ = [
    "GeminiAuthenticationError",
    "generate_chat_reply",
    "generate_response",
    "search_web_snippets",
    "API_KEY",
    "MODEL",
]
