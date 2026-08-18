import os

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

MONGO_URL = os.environ.get("MONGO_URL", "")

ADMIN_IDS = [
    int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x.strip().isdigit()
]

LOG_GROUP_ID = int(os.environ.get("LOG_GROUP_ID", "0"))

OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "")
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "")
SUPPORT_CHANNEL = os.environ.get("SUPPORT_CHANNEL", "")

START_IMAGE = os.environ.get("START_IMAGE", "")

SPAM_LIMIT = int(os.environ.get("SPAM_LIMIT", "5"))
SPAM_WINDOW = int(os.environ.get("SPAM_WINDOW", "7"))

REPLY_CHANCE = int(os.environ.get("REPLY_CHANCE", "20"))


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

    if missing:
        raise SystemExit(
            f"Missing required env vars: {', '.join(missing)}\n"
            f"   set config vars"
        )
