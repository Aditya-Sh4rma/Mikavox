"""
Mikasa/plugins/start.py
/start command:
  - Private chat: welcome image + caption + 2 rows of buttons
      Row 1: Support | Updates
      Row 2: Owner
    Naya user ho toh mongo mein save hota hai aur logger ko batata hai.
  - Group chat: alag (chhota) welcome message, group ko mongo mein save
    (agar pehli baar hai) — group-add wala log yahan nahi, wo
    ChatMemberUpdated handler (logger.py mein) automatically karta hai.
"""

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import OWNER_USERNAME, START_IMAGE, SUPPORT_CHANNEL, SUPPORT_CHAT
from Mikasa import mongo
from Mikasa.plugins.logger import log_user_start

PRIVATE_CAPTION = (
    "ကြိုဆိုပါတယ်ဗျာ 🪙\n"
    "အော်တိုစာပြန် BOT ဖြစ်ပါတယ် 🪙\n"
    "အသုံးပြုသည့်အတွက် ကျေးဇူးတင်ပါတယ် 🪙"
)

GROUP_CAPTION = (
    "မင်္ဂလာပါ! 🪙\n"
    "ဒီ Group ထဲမှာ Auto Reply Bot အသင့်ပါပဲ။"
)


def register(app: Client):

    @app.on_message(filters.command("start") & filters.private)
    async def start_private(client: Client, message: Message):
        is_new = await mongo.add_user(message.from_user.id)
        if is_new:
            await log_user_start(client, message.from_user)

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Support", url=SUPPORT_CHAT),
                    InlineKeyboardButton("Updates", url=SUPPORT_CHANNEL),
                ],
                [
                    InlineKeyboardButton("Owner", url=f"https://t.me/{OWNER_USERNAME}"),
                ],
            ]
        )

        if START_IMAGE:
            await client.send_photo(
                message.chat.id,
                START_IMAGE,
                caption=PRIVATE_CAPTION,
                reply_markup=buttons,
            )
        else:
            await message.reply_text(PRIVATE_CAPTION, reply_markup=buttons)

    @app.on_message(filters.command("start") & filters.group)
    async def start_group(client: Client, message: Message):
        await mongo.add_group(message.chat.id, message.chat.title or "")
        await message.reply_text(GROUP_CAPTION)
