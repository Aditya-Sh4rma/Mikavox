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
            "Usage: <code>/addsudo &lt;reply/@username/user_id&gt;</code>",
            parse_mode=enums.ParseMode.HTML,
        )

    if user.id == config.OWNER_ID:
        return await message.reply_text("Owner already has full access.")

    if message.command[0] == "addsudo":
        added = await add_sudo(user.id)
        if not added:
            return await message.reply_text(
                f"{user_mention(user)} is already a sudo user.",
                parse_mode=enums.ParseMode.HTML,
            )
        await message.reply_text(
            f"Added {user_mention(user)} to sudo users.",
            parse_mode=enums.ParseMode.HTML,
        )
    else:
        if user.id in config.ADMIN_IDS:
            return await message.reply_text(
                f"{user_mention(user)} is configured via <code>ADMIN_IDS</code> "
                "and cannot be removed from here.",
                parse_mode=enums.ParseMode.HTML,
            )

        removed = await remove_sudo(user.id)
        if not removed:
            return await message.reply_text(
                f"{user_mention(user)} is not a sudo user.",
                parse_mode=enums.ParseMode.HTML,
            )
        await message.reply_text(
            f"Removed {user_mention(user)} from sudo users.",
            parse_mode=enums.ParseMode.HTML,
        )


@app.on_message(filters.command(["listsudo", "sudolist"]))
async def _listsudo(client: Client, message: Message):
    sender_id = message.from_user.id if message.from_user else 0
    await load_sudoers()
    if not (is_owner(sender_id) or sender_id in get_sudo_ids()):
        return

    status = await message.reply_text("Fetching sudo users list...")

    lines = ["<b><u>Owner:</u></b>"]
    try:
        owner = await client.get_users(config.OWNER_ID)
        lines.append(f"- {user_mention(owner)}")
    except Exception:
        lines.append(f"- <code>{config.OWNER_ID}</code>")

    sudoers = [uid for uid in await mongo.get_sudoers() if uid != config.OWNER_ID]
    if sudoers:
        lines.append("")
        lines.append("<b><u>Sudo users:</u></b>")
        for user_id in sudoers:
            try:
                user = await client.get_users(user_id)
                lines.append(f"- {user_mention(user)}")
            except Exception:
                lines.append(f"- <code>{user_id}</code>")
    else:
        lines.append("")
        lines.append("<i>No sudo users added yet.</i>")

    await status.edit_text("\n".join(lines), parse_mode=enums.ParseMode.HTML)
