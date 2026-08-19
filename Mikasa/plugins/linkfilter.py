import re

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import ADMIN_IDS

link_pattern = re.compile(r"(https?://|t\.me/|www\.)")

# Burmese: "ဒီ group ထဲမှာ ကြော်ငြာ (Ads) ခွင့်မပြုပါ" -> "Is group me Ads Allowed nahi hai"
WARNING_TEXT = "⚠️ ဒီ Group ထဲမှာ Ads (ကြော်ငြာ) ခွင့်မပြုပါ။"

CLOSE_CALLBACK_DATA = "linkfilter_close"


def register(app: Client):

    @app.on_message(filters.text & filters.group & ~filters.regex(r"^/"))
    async def delete_links(client: Client, message: Message):
        if message.from_user is None:
            return

        sender_id = message.from_user.id
        chat_id = message.chat.id

        if sender_id in ADMIN_IDS:
            return

        try:
            member = await client.get_chat_member(chat_id, sender_id)
            if member.status in ("administrator", "creator"):
                return
        except Exception:
            pass

        text = (message.text or "").lower().strip()

        if not link_pattern.search(text):
            return

        try:
            await message.delete()
        except Exception:
            pass

        bot_username = client.me.username
        add_me_url = f"https://t.me/{bot_username}?startgroup=true"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➕ Add Me", url=add_me_url),
                    InlineKeyboardButton("✖️ Close", callback_data=CLOSE_CALLBACK_DATA),
                ]
            ]
        )

        try:
            await client.send_message(
                chat_id,
                WARNING_TEXT,
                reply_markup=keyboard,
            )
        except Exception:
            pass

    @app.on_callback_query(filters.regex(f"^{CLOSE_CALLBACK_DATA}$"))
    async def close_warning(client: Client, callback_query: CallbackQuery):
        try:
            await callback_query.message.delete()
        except Exception:
            pass
        try:
            await callback_query.answer()
        except Exception:
            pass
