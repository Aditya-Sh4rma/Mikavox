import os

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

MONGO_URL = os.environ.get("MONGO_URL", "")

OWNER_ID = int(os.environ.get("OWNER_ID", "0") or 0)

LOG_GROUP_ID = int(os.environ.get("LOG_GROUP_ID", "0"))

OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "itz_m4rvin")
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "https://t.me/SamuraisSupport")
SUPPORT_CHANNEL = os.environ.get("SUPPORT_CHANNEL", "https://t.me/SamuraisSupport")

START_IMAGE = os.environ.get("START_IMAGE", "")


def validate():
    missing = []

    if not API_ID:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not MONGO_URL:
        missing.append("MONGO_URL")
    if not OWNER_ID:
        missing.append("OWNER_ID")

    if missing:
        raise SystemExit(f"Missing required env vars: {', '.join(missing)}")
