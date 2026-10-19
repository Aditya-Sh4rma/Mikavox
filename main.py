from pyrogram import enums, idle

from config import LOG_GROUP_ID
from Mikasa import app


async def main():
    await app.start()
    print("Bot started")

    if LOG_GROUP_ID:
        try:
            await app.send_message(
                LOG_GROUP_ID,
                "<b>Bot started</b>",
                parse_mode=enums.ParseMode.HTML,
            )
        except Exception:
            pass

    await idle()
    await app.stop()


if __name__ == "__main__":
    app.run(main())
