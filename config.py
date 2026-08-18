"""
config.py
Saari environment variables yahan se load hoti hain.
Baaki koi file mein direct os.environ nahi likhna — yahi se import karo.
"""

import os

# Telegram API credentials (my.telegram.org se milte hain)
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# MongoDB Atlas connection string
MONGO_URL = os.environ.get("MONGO_URL", "")

# Admin user IDs (env mein comma-separated, e.g. "123456,789012")
ADMIN_IDS = [
    int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x.strip().isdigit()
]

# Log group — jahan start / group-add / group-remove logs jaayenge
LOG_GROUP_ID = int(os.environ.get("LOG_GROUP_ID", "0"))

# /start message ke buttons ke liye (private chat mein)
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "")    # bina @ ke, e.g. "TG_yi5"
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "")         # full t.me link
SUPPORT_CHANNEL = os.environ.get("SUPPORT_CHANNEL", "")   # full t.me link

# /start image
START_IMAGE = os.environ.get("START_IMAGE", "")

# Anti-spam settings
SPAM_LIMIT = int(os.environ.get("SPAM_LIMIT", "5"))    # messages
SPAM_WINDOW = int(os.environ.get("SPAM_WINDOW", "7"))   # seconds

# Default reply trigger chance (%) — 20 matlab ~20% messages par reply aayega
REPLY_CHANCE = int(os.environ.get("REPLY_CHANCE", "20"))


def validate():
    """Startup pe check karta hai ki zaroori vars set hain ya nahi.
    Missing hone par turant clear error deke ruk jaata hai, taaki bot
    silently crash na ho aur pata chal jaaye kya missing hai."""
    missing = []
    if not API_ID:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not MONGO_URL:
        missing.append("MONGO_URL")

    if missing:
        raise SystemExit(
            f"❌ Missing required env vars: {', '.join(missing)}\n"
            f"   .env.example dekho ya Heroku Config Vars set karo."
        )
