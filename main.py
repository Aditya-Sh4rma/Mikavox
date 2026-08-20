from pyrogram import Client

import config
from Mikasa.plugins import broadcast, linkfilter, logger, reply, start, stats

config.validate()

app = Client(
    "mikasa",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

start.register(app)
linkfilter.register(app)
reply.register(app)
broadcast.register(app)
stats.register(app)
logger.register(app)

if __name__ == "__main__":
    print("Mikasa Bot Running...")
    app.run()
