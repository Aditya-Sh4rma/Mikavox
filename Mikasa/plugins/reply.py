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
from Mikasa.emoji import PREMIUM_EMOJIS, get_random_emoji_html

_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(_ROOT_DIR, "replies.json"), "r", encoding="utf-8") as f:
    DEFAULT_REPLIES: list[str] = json.load(f)

with open(os.path.join(_ROOT_DIR, "smart_replies.json"), "r", encoding="utf-8") as f:
    SMART_REPLIES: dict[str, list[str]] = json.load(f)

print(
    f"[reply.py] Cached {len(DEFAULT_REPLIES)} default replies, "
    f"{len(SMART_REPLIES)} smart-reply keywords."
)

warns = defaultdict(int)
muted_users: set[int] = set()
user_messages = defaultdict(lambda: deque(maxlen=SPAM_LIMIT))

group_msg_count: dict[int, int] = defaultdict(int)
group_threshold: dict[int, int] = {}

link_pattern = re.compile(r"(https?://|t\.me/|www\.)")


def _get_threshold(chat_id: int) -> int:
    if chat_id not in group_threshold:
        group_threshold[chat_id] = random.randint(20, 30)
    return group_threshold[chat_id]


async def _send_with_emoji(message: Message, text: str):
    emoji_tag = get_random_emoji_html()
    final_text = f"{emoji_tag} {text}" if emoji_tag else text
    await message.reply_text(final_text, parse_mode=ParseMode.HTML)


async def _react(client: Client, message: Message):
    if PREMIUM_EMOJIS:
        emoji_char, emoji_id = random.choice(list(PREMIUM_EMOJIS.items()))
        try:
            await client.send_reaction(
                chat_id=message.chat.id,
                message_id=message.id,
                emoji=int(emoji_id),
            )
            return
        except Exception:
            pass

    try:
        await client.send_reaction(
            chat_id=message.chat.id,
            message_id=message.id,
            emoji="❤️",
        )
    except Exception:
        pass


def register(app: Client):

    @app.on_message(filters.text & ~filters.command(""))
    async def auto_reply(client: Client, message: Message):
        if message.from_user is None:
            return

        sender_id = message.from_user.id
        chat_id = message.chat.id

        if sender_id in ADMIN_IDS:
            return

        if message.chat.type in ("group", "supergroup"):
            try:
                member = await client.get_chat_member(chat_id, sender_id)
                if member.status in ("administrator", "creator"):
                    return
            except Exception:
                pass

        if sender_id in muted_users:
            return

        text = (message.text or "").lower().strip()

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

        if link_pattern.search(text):
            try:
                await message.delete()
            except Exception:
                pass
            return

        is_reply_to_bot = (
            message.reply_to_message is not None
            and message.reply_to_message.from_user is not None
            and message.reply_to_message.from_user.id == client.me.id
        )

        if is_reply_to_bot:
            if DEFAULT_REPLIES:
                await asyncio.sleep(random.randint(1, 3))
                await _send_with_emoji(message, random.choice(DEFAULT_REPLIES))
                await _react(client, message)
            return

        for key, replies in SMART_REPLIES.items():
            if key.lower() in text:
                await asyncio.sleep(random.randint(1, 3))
                await _send_with_emoji(message, random.choice(replies))
                await _react(client, message)
                return

        if DEFAULT_REPLIES and random.randint(1, 100) <= REPLY_CHANCE:
            await asyncio.sleep(random.randint(2, 5))
            await _send_with_emoji(message, random.choice(DEFAULT_REPLIES))
            await _react(client, message)
            return

        if message.chat.type in ("group", "supergroup"):
            group_msg_count[chat_id] += 1
            if group_msg_count[chat_id] >= _get_threshold(chat_id):
                group_msg_count[chat_id] = 0
                group_threshold.pop(chat_id, None)

                if PREMIUM_EMOJIS:
                    emoji_char, emoji_id = random.choice(list(PREMIUM_EMOJIS.items()))
                    emoji_tag = f'<emoji id="{emoji_id}">{emoji_char}</emoji>'
                    try:
                        await client.send_message(
                            chat_id, emoji_tag, parse_mode=ParseMode.HTML
                        )
                    except Exception:
                        pass
