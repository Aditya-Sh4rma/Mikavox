from pyrogram import Client, enums, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import OWNER_USERNAME, START_IMAGE, SUPPORT_CHANNEL, SUPPORT_CHAT
from Mikasa import app, mongo
from Mikasa.plugins.logger import log_user_start

PRIVATE_CAPTION = (
    "မင်္ဂလာပါ! ဒီ Bot က Group ထဲမှာ အလိုအလျောက် စာပြန်ပေးပါတယ်။\n"
    "Premium emoji, sticker နဲ့ link ဖျက်ပေးတာတွေလည်း လုပ်ပေးပါတယ်။\n\n"
    "အောက်က button နဲ့ သင့် Group ထဲ ထည့်လိုက်ပါ။"
)

GROUP_CAPTION = "မင်္ဂလာပါ! ဒီ Group ထဲမှာ Auto Reply Bot အသင့်ပါပဲ။"


@app.on_message(filters.command("start") & filters.private)
async def start_private(client: Client, message: Message):
    is_new = await mongo.add_user(message.from_user.id)
    if is_new:
        await log_user_start(client, message.from_user)

    bot = await client.get_me()
    bot_username = bot.username

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Add Me In Your Group",
                    url=f"https://t.me/{bot_username}?startgroup=true",
                    style=enums.ButtonStyle.PRIMARY,
                )
            ],
            [
                InlineKeyboardButton(
                    "Support",
                    url=SUPPORT_CHAT,
                    style=enums.ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    "Updates",
                    url=SUPPORT_CHANNEL,
                    style=enums.ButtonStyle.PRIMARY,
                ),
            ],
            [
                InlineKeyboardButton(
                    "Owner",
                    url=f"https://t.me/{OWNER_USERNAME}",
                    style=enums.ButtonStyle.PRIMARY,
                )
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
