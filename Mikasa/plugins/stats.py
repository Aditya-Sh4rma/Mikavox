from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from Mikasa import mongo


def register(app: Client):

    @app.on_message(filters.command("stats"))
    async def stats(client: Client, message: Message):
        users = await mongo.total_users()
        groups = await mongo.total_groups()

        await message.reply_text(
            "<b>Mikasa Stats</b>\n\n"
            f"Total Users: <code>{users}</code>\n"
            f"Total Groups: <code>{groups}</code>",
            parse_mode=ParseMode.HTML,
        )
