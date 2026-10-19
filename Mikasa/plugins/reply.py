import asyncio
import json
import os
import random

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from Mikasa import app
from Mikasa.emoji import get_random_emoji_html
from Mikasa.sticker import get_random_sticker

_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(_ROOT_DIR, "replies.json"), "r", encoding="utf-8") as f:
    DEFAULT_REPLIES: list[str] = json.load(f)

with open(os.path.join(_ROOT_DIR, "prm_replies.json"), "r", encoding="utf-8") as f:
    PRM_REPLIES: dict[str, list[str]] = json.load(f)

GROUP_REPLY_DELAY = 1

group_msg_count: dict[int, int] = {}
group_threshold: dict[int, int] = {}

MIKASA_KEYWORD = "mikasa"

_STRIP_CHARS = ".,!?;:\"'()[]{}"


def _get_threshold(chat_id: int) -> int:
    if chat_id not in group_threshold:
        group_threshold[chat_id] = random.randint(20, 30)
    return group_threshold[chat_id]


def _match_prm_keyword(text: str) -> str | None:
    for token in text.split():
        cleaned = token.strip(_STRIP_CHARS)
        if cleaned in PRM_REPLIES:
            return cleaned
    return None


async def _send_with_emoji(message: Message, text: str):
    emoji_tag = get_random_emoji_html()
    final_text = f"{text} {emoji_tag}" if emoji_tag else text
    await message.reply_text(final_text, parse_mode=ParseMode.HTML)


async def _group_delay(message: Message):
    if message.chat.type in ("group", "supergroup"):
        await asyncio.sleep(GROUP_REPLY_DELAY)


@app.on_message(filters.text & ~filters.regex(r"^/"))
async def auto_reply(client: Client, message: Message):
    if message.from_user is None:
        return

    sender_id = message.from_user.id
    chat_id = message.chat.id

    if message.chat.type in ("group", "supergroup"):
        try:
            member = await client.get_chat_member(chat_id, sender_id)
            if member.status in ("administrator", "creator"):
                return
        except Exception:
            pass

    text = (message.text or "").lower().strip()

    matched_key = _match_prm_keyword(text)
    if matched_key:
        await _group_delay(message)
        await _send_with_emoji(message, random.choice(PRM_REPLIES[matched_key]))
        return

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
        return

    if message.chat.type in ("group", "supergroup"):
        group_msg_count[chat_id] = group_msg_count.get(chat_id, 0) + 1
        if group_msg_count[chat_id] >= _get_threshold(chat_id):
            group_msg_count[chat_id] = 0
            group_threshold.pop(chat_id, None)

            emoji_tag = get_random_emoji_html()
            if emoji_tag:
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
