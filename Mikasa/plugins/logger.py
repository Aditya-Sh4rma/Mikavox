from pyrogram import Client, enums, filters
from pyrogram.types import Message, User

from config import LOG_GROUP_ID
from Mikasa import app, mongo


async def log_user_start(client: Client, user: User):
    if not LOG_GROUP_ID:
        return

    name = user.first_name or "Unknown"
    username = f"@{user.username}" if user.username else "(no username)"

    await client.send_message(
        LOG_GROUP_ID,
        f"<b>New user started the bot</b>\n"
        f"User: {name} {username}\n"
        f"ID: <code>{user.id}</code>",
        parse_mode=enums.ParseMode.HTML,
    )


async def log_group_add(
    client: Client, chat_id: int, chat_title: str, added_by: User | None
):
    if not LOG_GROUP_ID:
        return

    by = (
        f"{added_by.first_name} (@{added_by.username})"
        if added_by and added_by.username
        else "Unknown"
    )

    await client.send_message(
        LOG_GROUP_ID,
        f"<b>Bot added to group</b>\n"
        f"Group: {chat_title}\n"
        f"ID: <code>{chat_id}</code>\n"
        f"Added by: {by}",
        parse_mode=enums.ParseMode.HTML,
    )


async def log_group_remove(
    client: Client, chat_id: int, chat_title: str, removed_by: User | None
):
    if not LOG_GROUP_ID:
        return

    by = (
        f"{removed_by.first_name} (@{removed_by.username})"
        if removed_by and removed_by.username
        else "Unknown"
    )

    await client.send_message(
        LOG_GROUP_ID,
        f"<b>Bot removed from group</b>\n"
        f"Group: {chat_title}\n"
        f"ID: <code>{chat_id}</code>\n"
        f"Removed by: {by}",
        parse_mode=enums.ParseMode.HTML,
    )


@app.on_message(filters.new_chat_members, group=7)
async def _bot_added(client: Client, message: Message):
    for member in message.new_chat_members:
        if member.id != client.me.id:
            continue

        chat_id = message.chat.id
        chat_title = message.chat.title or ""

        is_new = await mongo.add_group(chat_id, chat_title)
        if is_new:
            await log_group_add(client, chat_id, chat_title, message.from_user)


@app.on_message(filters.left_chat_member, group=8)
async def _bot_removed(client: Client, message: Message):
    if message.left_chat_member is None:
        return

    if message.left_chat_member.id != client.me.id:
        return

    chat_id = message.chat.id
    chat_title = message.chat.title or ""

    await mongo.remove_group(chat_id)
    await log_group_remove(client, chat_id, chat_title, message.from_user)
