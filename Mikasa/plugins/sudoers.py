from pyrogram import Client, enums, filters
from pyrogram.types import Message

import config
from Mikasa import app, mongo
from Mikasa.sudo import (
    add_sudo,
    get_sudo_ids,
    is_owner,
    load_sudoers,
    owner_filter,
    remove_sudo,
)
from Mikasa.utils import extract_user, user_mention


@app.on_message(filters.command(["addsudo", "delsudo", "rmsudo"]) & owner_filter)
async def _sudo(client: Client, message: Message):
    await load_sudoers()

    user = await extract_user(client, message)
    if not user:
        return await message.reply_text(
            "Reply to a user or send a username or user id.\n"
            "Example: <code>/addsudo @username</code>",
            parse_mode=enums.ParseMode.HTML,
        )

    if user.id == config.OWNER_ID:
        return await message.reply_text("Owner already has full access.")

    if message.command[0] == "addsudo":
        added = await add_sudo(user.id)
        if not added:
            return await message.reply_text(
                f"{user_mention(user)} already has sudo access.",
                parse_mode=enums.ParseMode.HTML,
            )
        await message.reply_text(
            f"{user_mention(user)} now has sudo access.",
            parse_mode=enums.ParseMode.HTML,
        )
    else:
        removed = await remove_sudo(user.id)
        if not removed:
            return await message.reply_text(
                f"{user_mention(user)} does not have sudo access.",
                parse_mode=enums.ParseMode.HTML,
            )
        await message.reply_text(
            f"{user_mention(user)} no longer has sudo access.",
            parse_mode=enums.ParseMode.HTML,
        )


@app.on_message(filters.command(["listsudo", "sudolist"]))
async def _listsudo(client: Client, message: Message):
    sender_id = message.from_user.id if message.from_user else 0
    await load_sudoers()
    if not (is_owner(sender_id) or sender_id in get_sudo_ids()):
        return

    status = await message.reply_text("Loading list...")

    try:
        owner = await client.get_users(config.OWNER_ID)
        owner_text = user_mention(owner)
    except Exception:
        owner_text = f"<code>{config.OWNER_ID}</code>"

    names = []
    for user_id in await mongo.get_sudoers():
        if user_id == config.OWNER_ID:
            continue
        try:
            user = await client.get_users(user_id)
            names.append(user_mention(user))
        except Exception:
            names.append(f"<code>{user_id}</code>")

    sudo_text = ", ".join(names) if names else "none"

    await status.edit_text(
        f"<b>Bot access</b>\n\nOwner: {owner_text}\nSudo: {sudo_text}",
        parse_mode=enums.ParseMode.HTML,
    )
