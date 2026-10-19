import re

from pyrogram import Client, enums
from pyrogram.types import Message, User


async def extract_user(client: Client, message: Message) -> User | None:
    if message.reply_to_message and message.reply_to_message.from_user:
        return message.reply_to_message.from_user

    if message.entities:
        for entity in message.entities:
            if entity.type == enums.MessageEntityType.TEXT_MENTION and entity.user:
                return entity.user

    if message.text:
        args = message.text.split(None, 1)
        arg = args[1].strip() if len(args) > 1 else ""

        if arg:
            try:
                if arg.startswith("@"):
                    return await client.get_users(arg)
                if re.fullmatch(r"-?\d{5,15}", arg):
                    return await client.get_users(int(arg))
            except Exception:
                return None

    return None


def user_mention(user: User) -> str:
    name = user.first_name or "User"
    return f'<a href="tg://user?id={user.id}">{name}</a>'
