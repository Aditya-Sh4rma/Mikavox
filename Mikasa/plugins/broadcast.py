import asyncio
import os

from pyrogram import Client, enums, errors, filters
from pyrogram.types import Message

from Mikasa import app, mongo
from Mikasa.sudo import load_sudoers, sudo_filter

broadcasting = asyncio.Lock()
_stop_requested = False


def _parse_args(message: Message) -> tuple[set[str], str | None]:
    raw = message.text or message.caption or ""
    parts = raw.split(None, 1)
    if len(parts) < 2:
        return set(), None

    words = parts[1].split()
    flags: set[str] = set()
    text_words: list[str] = []

    for word in words:
        if word.lower() in ("-user", "-nochat", "-copy"):
            flags.add(word.lower())
        else:
            text_words.append(word)

    text = " ".join(text_words) if text_words else None
    return flags, text


async def _send(
    client: Client,
    source: Message | None,
    text: str | None,
    chat_id: int,
    copy: bool,
):
    if source is not None:
        if copy:
            await source.copy(chat_id, reply_markup=source.reply_markup)
        else:
            await source.forward(chat_id)
    else:
        await client.send_message(chat_id, text)


@app.on_message(filters.command("broadcast") & sudo_filter)
async def broadcast(client: Client, message: Message):
    await load_sudoers()

    flags, text = _parse_args(message)
    source = message.reply_to_message

    if source is None and not text:
        return await message.reply_text(
            "<b>Usage:</b>\n"
            "<code>/broadcast &lt;text&gt;</code>\n"
            "<code>/broadcast</code> (reply to a message)\n\n"
            "<b>Flags:</b>\n"
            "<code>-user</code> send to users\n"
            "<code>-nochat</code> skip groups\n"
            "<code>-copy</code> copy instead of forward",
            parse_mode=enums.ParseMode.HTML,
        )

    global _stop_requested

    if broadcasting.locked():
        return await message.reply_text(
            "A broadcast is already running. Use /stopbroadcast to stop it."
        )

    await broadcasting.acquire()
    _stop_requested = False

    try:
        include_users = "-user" in flags
        include_chats = "-nochat" not in flags
        copy = "-copy" in flags

        chat_ids = await mongo.all_group_ids() if include_chats else []
        user_ids = await mongo.all_user_ids() if include_users else []
        targets = [(cid, "chat") for cid in chat_ids] + [
            (uid, "user") for uid in user_ids
        ]

        if not targets:
            return await message.reply_text(
                "No targets found. Check the flags: groups are skipped with "
                "-nochat, users need -user."
            )

        status = await message.reply_text(
            f"Broadcasting to {len(chat_ids)} groups + {len(user_ids)} users..."
        )

        sent_chats, sent_users, failed = 0, 0, []
        failed_lines: list[str] = []

        for chat_id, kind in targets:
            if _stop_requested:
                break

            try:
                await _send(client, source, text, chat_id, copy)
                if kind == "chat":
                    sent_chats += 1
                else:
                    sent_users += 1
                await asyncio.sleep(0.1)
            except errors.FloodWait as fw:
                await asyncio.sleep(fw.value + 10)
            except Exception as ex:
                failed.append(chat_id)
                failed_lines.append(f"{chat_id} - {ex}")
                continue

        stopped = " (stopped)" if _stop_requested else ""
        result = (
            f"Broadcast done{stopped}.\n"
            f"Sent: {sent_chats} groups + {sent_users} users\n"
            f"Failed: {len(failed)}"
        )

        if failed_lines:
            try:
                path = "broadcast_errors.txt"
                with open(path, "w", encoding="utf-8") as f:
                    f.write("\n".join(failed_lines))
                await message.reply_document(path, caption=result)
                os.remove(path)
            except Exception:
                await status.edit_text(result)
        else:
            await status.edit_text(result)
    finally:
        broadcasting.release()


@app.on_message(filters.command(["stopbroadcast", "stop_gcast"]) & sudo_filter)
async def stop_broadcast(client: Client, message: Message):
    global _stop_requested

    if not broadcasting.locked():
        return await message.reply_text("No broadcast is running.")

    _stop_requested = True
    await message.reply_text("Broadcast stop requested. It will stop after the current send.")
