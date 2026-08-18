"""
Mikasa/plugins/broadcast.py
/broadcast <message>  -> sirf ADMIN_IDS use kar sakte hain.
Sab saved users + sab saved groups ko message bhejta hai.
Har send ke beech chhota sa delay hai taaki Telegram flood-limit na lage.
"""

import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from config import ADMIN_IDS
from Mikasa import mongo


def register(app: Client):

    @app.on_message(filters.command("broadcast") & filters.user(ADMIN_IDS))
    async def broadcast(client: Client, message: Message):
        if len(message.command) < 2 and not message.reply_to_message:
            await message.reply_text(
                "Usage: /broadcast <message>\n"
                "Ya kisi message ko reply karke /broadcast likho."
            )
            return

        # Reply kiye gaye message ko forward karenge, warna text bhejenge
        source_text = None
        source_message = None
        if message.reply_to_message:
            source_message = message.reply_to_message
        else:
            source_text = message.text.split(None, 1)[1]

        user_ids = await mongo.all_user_ids()
        group_ids = await mongo.all_group_ids()
        targets = user_ids + group_ids

        status = await message.reply_text(
            f"📤 Broadcasting to {len(user_ids)} users + {len(group_ids)} groups..."
        )

        sent, failed = 0, 0
        for chat_id in targets:
            try:
                if source_message:
                    await source_message.copy(chat_id)
                else:
                    await client.send_message(chat_id, source_text)
                sent += 1
            except Exception:
                failed += 1
            await asyncio.sleep(0.1)  # flood-wait se bachne ke liye

        await status.edit_text(f"✅ Broadcast done.\nSent: {sent} | Failed: {failed}")
