from pyrogram import Client
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import ChatMemberUpdated, User

from config import LOG_GROUP_ID
from Mikasa import mongo


async def log_user_start(client: Client, user: User):
    if not LOG_GROUP_ID:
        return
    name = user.first_name or "Unknown"
    username = f"@{user.username}" if user.username else "(no username)"
    await client.send_message(
        LOG_GROUP_ID,
        f"🟢 <b>New Bot Start</b>\n"
        f"User: {name} {username}\n"
        f"ID: <code>{user.id}</code>",
        parse_mode=ParseMode.HTML,
    )


async def log_group_add(client: Client, chat_id: int, chat_title: str, added_by: User | None):
    if not LOG_GROUP_ID:
        return
    by = f"{added_by.first_name} (@{added_by.username})" if added_by and added_by.username else "Unknown"
    await client.send_message(
        LOG_GROUP_ID,
        f"➕ <b>Bot Added to Group</b>\n"
        f"Group: {chat_title}\n"
        f"ID: <code>{chat_id}</code>\n"
        f"Added by: {by}",
        parse_mode=ParseMode.HTML,
    )


async def log_group_remove(client: Client, chat_id: int, chat_title: str, removed_by: User | None):
    if not LOG_GROUP_ID:
        return
    by = f"{removed_by.first_name} (@{removed_by.username})" if removed_by and removed_by.username else "Unknown"
    await client.send_message(
        LOG_GROUP_ID,
        f"➖ <b>Bot Removed from Group</b>\n"
        f"Group: {chat_title}\n"
        f"ID: <code>{chat_id}</code>\n"
        f"Removed by: {by}",
        parse_mode=ParseMode.HTML,
    )


def register(app: Client):

    @app.on_chat_member_updated()
    async def on_member_update(client: Client, update: ChatMemberUpdated):
        if update.new_chat_member is None:
            return
        if update.new_chat_member.user.id != client.me.id:
            return

        chat_id = update.chat.id
        chat_title = update.chat.title or ""
        old_status = update.old_chat_member.status if update.old_chat_member else None
        new_status = update.new_chat_member.status

        was_member = old_status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR)
        is_member = new_status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR)

        if not was_member and is_member:
            is_new = await mongo.add_group(chat_id, chat_title)
            if is_new:
                await log_group_add(client, chat_id, chat_title, update.from_user)

        elif was_member and not is_member:
            await mongo.remove_group(chat_id)
            await log_group_remove(client, chat_id, chat_title, update.from_user)
