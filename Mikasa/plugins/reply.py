import asyncio
import json
import os
import random

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from config import ADMIN_IDS
from Mikasa.emoji import PREMIUM_EMOJIS, get_random_emoji_html
from Mikasa.sticker import get_random_sticker

_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(_ROOT_DIR, "replies.json"), "r", encoding="utf-8") as f:
    DEFAULT_REPLIES: list[str] = json.load(f)

# DEFAULT_REPLIES aur PREMIUM_EMOJIS dono module-import ke time hi load ho jaate
# hain (upar wala `with open(...)` aur emoji.py ke andar wala dict), isliye
# ye dono already in-memory cached hain -- runtime pe koi disk/network read nahi hota.
print(f"[reply.py] Cached {len(DEFAULT_REPLIES)} default replies, {len(PREMIUM_EMOJIS)} premium emojis.")

GROUP_REPLY_DELAY = 1  # seconds -- har group reply se pehle fixed gap

group_msg_count: dict[int, int] = {}
group_threshold: dict[int, int] = {}

MIKASA_KEYWORD = "mikasa"


def _get_threshold(chat_id: int) -> int:
    if chat_id not in group_threshold:
        group_threshold[chat_id] = random.randint(20, 30)
    return group_threshold[chat_id]


async def _send_with_emoji(message: Message, text: str):
    emoji_tag = get_random_emoji_html()
    # Emoji ab message ke BAAD aayega (pehle "emoji message" tha, ab "message emoji")
    final_text = f"{text} {emoji_tag}" if emoji_tag else text
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


async def _group_delay(message: Message):
    """Group/supergroup me har reply se pehle fixed 1-second gap."""
    if message.chat.type in ("group", "supergroup"):
        await asyncio.sleep(GROUP_REPLY_DELAY)


def register(app: Client):

    @app.on_message(filters.text & ~filters.regex(r"^/"))
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

        text = (message.text or "").lower().strip()

        is_reply_to_bot = (
            message.reply_to_message is not None
            and message.reply_to_message.from_user is not None
            and message.reply_to_message.from_user.id == client.me.id
        )
        is_mikasa_mention = MIKASA_KEYWORD in text

        if is_reply_to_bot or is_mikasa_mention:
            if DEFAULT_REPLIES:
                await _group_delay(message)
                await _send_with_emoji(message, random.choice(DEFAULT_REPLIES))
                await _react(client, message)
            return

        # Group activity counter -- ab HAR text message pe increment hota hai.
        # Pehle ye sirf un messages pe increment hota tha jab upar koi bhi trigger
        # match na hua ho (spam/link/reply-to-bot/smart-reply/random-chance sab miss),
        # isliye ye sirf ~20-30% messages pe hi badhta tha aur threshold tak
        # reliably kabhi pahuchta nahi tha -- yahi bug tha jiski wajah se
        # beech-beech wala standalone premium emoji message kaam nahi kar raha tha.
        if message.chat.type in ("group", "supergroup"):
            group_msg_count[chat_id] = group_msg_count.get(chat_id, 0) + 1
            if group_msg_count[chat_id] >= _get_threshold(chat_id):
                group_msg_count[chat_id] = 0
                group_threshold.pop(chat_id, None)

                if PREMIUM_EMOJIS:
                    emoji_char, emoji_id = random.choice(list(PREMIUM_EMOJIS.items()))
                    emoji_tag = f'<emoji id="{emoji_id}">{emoji_char}</emoji>'
                    try:
                        await _group_delay(message)
                        await client.send_message(
                            chat_id, emoji_tag, parse_mode=ParseMode.HTML
                        )
                    except Exception:
                        pass

    @app.on_message(filters.sticker & ~filters.regex(r"^/"))
    async def sticker_reply(client: Client, message: Message):
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

        is_reply_to_bot = (
            message.reply_to_message is not None
            and message.reply_to_message.from_user is not None
            and message.reply_to_message.from_user.id == client.me.id
        )

        if not is_reply_to_bot:
            return

        sticker_id = get_random_sticker()
        if not sticker_id:
            return

        await _group_delay(message)
        try:
            await message.reply_sticker(sticker_id)
        except Exception:
            pass
        await _react(client, message)
