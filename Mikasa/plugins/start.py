from pyrogram import Client, enums, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import OWNER_USERNAME, START_IMAGE, SUPPORT_CHANNEL, SUPPORT_CHAT
from Mikasa import app, mongo
from Mikasa.plugins.logger import log_user_start

PRIVATE_CAPTION = (
    "မင်္ဂလာပါ! ကျွန်တော် Mikasa ပါ။ 🪙\n\n"
    "Group ထဲမှာ အလိုအလျောက် စာပြန်ပေးတဲ့ Bot ပါ။\n\n"
    "• စကားပြောရင် အလိုအလျောက် ပြန်ဖြေပေးမယ်\n"
    "• “mikasa” လို့ ရေးရင် ဒါမှမဟုတ် ကျွန်တော့်ကို reply လုပ်ရင် ပြန်ဖြေမယ်\n"
    "• Premium emoji နဲ့ sticker တွေ ပို့ပေးမယ်\n"
    "• Link တွေ (Ads) ကို ဖျက်ပေးမယ်\n\n"
    "အောက်က button နဲ့ သင့် Group ထဲကို ထည့်လိုက်ပါ။\n"
    "အသုံးပြုပေးတဲ့အတွက် ကျေးဇူးတင်ပါတယ်။"
)

GROUP_CAPTION = (
    "မင်္ဂလာပါ! 🪙\n"
    "ဒီ Group ထဲမှာ Auto Reply Bot အသင့်ပါပဲ။"
)


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
