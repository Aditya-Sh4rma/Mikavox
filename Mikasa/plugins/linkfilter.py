import re

from pyrogram import Client, enums, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import ADMIN_IDS
from Mikasa import app
from Mikasa.sudo import is_sudo, load_sudoers

link_pattern = re.compile(r"(https?://|t\.me/|www\.)")

WARNING_TEXT = "⚠️ ဒီ Group ထဲမှာ Ads (ကြော်ငြာ) ခွင့်မပြုပါ။"

CLOSE_CALLBACK_DATA = "linkfilter_close"


@app.on_message(filters.text & filters.group & ~filters.regex(r"^/"), group=-1)
async def delete_links(client: Client, message: Message):
    if message.from_user is None:
        return

    sender_id = message.from_user.id
    chat_id = message.chat.id

    if sender_id in ADMIN_IDS:
        return

    await load_sudoers()
    if is_sudo(sender_id):
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

    add_me_url = f"https://t.me/{client.me.username}?startgroup=true"

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Add Me",
                    url=add_me_url,
                    style=enums.ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    "Close",
                    callback_data=CLOSE_CALLBACK_DATA,
                    style=enums.ButtonStyle.DANGER,
                ),
            ]
        ]
    )

    try:
        await client.send_message(chat_id, WARNING_TEXT, reply_markup=keyboard)
    except Exception:
        pass

    message.stop_propagation()


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
