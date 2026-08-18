"""
Mikasa/plugins/reply.py
Auto-reply system:
  - Startup pe replies.json + smart_replies.json (root mein) ek baar load
    hoke memory mein cache ho jaate hain (disk dobara nahi chuena, fast rahega)
  - Anti-spam + anti-link
  - Har reply ke aage ek random premium emoji lagta hai (Mikasa/emoji.py se)
"""

import asyncio
import json
import os
import random
import re
import time
from collections import defaultdict, deque

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from config import ADMIN_IDS, REPLY_CHANCE, SPAM_LIMIT, SPAM_WINDOW
from Mikasa.emoji import get_random_emoji_html

# =============================
# CACHE — startup par ek baar load, phir sirf memory se
# Root folder mein replies.json / smart_replies.json hain (Mikasa/ ke bahar),
# isliye path do folder upar jaake dhundhta hai.
# =============================
_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(_ROOT_DIR, "replies.json"), "r", encoding="utf-8") as f:
    DEFAULT_REPLIES: list[str] = json.load(f)

with open(os.path.join(_ROOT_DIR, "smart_replies.json"), "r", encoding="utf-8") as f:
    SMART_REPLIES: dict[str, list[str]] = json.load(f)

print(
    f"[reply.py] Cached {len(DEFAULT_REPLIES)} default replies, "
    f"{len(SMART_REPLIES)} smart-reply keywords."
)

# =============================
# RUNTIME STATE
# =============================
warns = defaultdict(int)
muted_users: set[int] = set()
user_messages = defaultdict(lambda: deque(maxlen=SPAM_LIMIT))

link_pattern = re.compile(r"(https?://|t\.me/|www\.)")


async def _send_with_emoji(message: Message, text: str):
    """Premium emoji ko reply ke aage lagata hai, phir HTML mode mein bhejta hai."""
    emoji_tag = get_random_emoji_html()
    final_text = f"{emoji_tag} {text}" if emoji_tag else text
    await message.reply_text(final_text, parse_mode=ParseMode.HTML)


def register(app: Client):

    @app.on_message(filters.text & ~filters.command(""))
    async def auto_reply(client: Client, message: Message):
        if message.from_user is None:
            return

        sender_id = message.from_user.id

        # Admin skip
        if sender_id in ADMIN_IDS:
            return

        # Group admin skip
        if message.chat.type in ("group", "supergroup"):
            try:
                member = await client.get_chat_member(message.chat.id, sender_id)
                if member.status in ("administrator", "creator"):
                    return
            except Exception:
                pass

        # Muted user skip
        if sender_id in muted_users:
            return

        text = (message.text or "").lower().strip()

        # ---- Anti-spam ----
        now = time.time()
        user_messages[sender_id].append(now)

        if len(user_messages[sender_id]) >= SPAM_LIMIT:
            if now - user_messages[sender_id][0] < SPAM_WINDOW:
                warns[sender_id] += 1
                await message.reply_text("⚠️ Spam မလုပ်ပါနဲ့")

                if warns[sender_id] >= 3:
                    muted_users.add(sender_id)
                    await message.reply_text("🔇 Spam ကြောင့် Mute လုပ်လိုက်ပါပြီ")
                return

        # ---- Anti-link ----
        if link_pattern.search(text):
            try:
                await message.delete()
            except Exception:
                pass
            return

        # ---- Smart reply (keyword match) ----
        for key, replies in SMART_REPLIES.items():
            if key.lower() in text:
                await asyncio.sleep(random.randint(1, 3))
                await _send_with_emoji(message, random.choice(replies))
                return

        # ---- Default reply (random chance) ----
        if DEFAULT_REPLIES and random.randint(1, 100) <= REPLY_CHANCE:
            await asyncio.sleep(random.randint(2, 5))
            await _send_with_emoji(message, random.choice(DEFAULT_REPLIES))
