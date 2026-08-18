"""
main.py
Entry point (root mein). `python main.py` se chalta hai, Procfile bhi isi ko call karta hai.

Kya karta hai:
  1. config.validate() — zaroori env vars check karta hai, missing hone par
     turant clear error deke rukta hai (silent crash nahi).
  2. Pyrogram Client banata hai.
  3. Har plugin ka register(app) function call karta hai (Mikasa/plugins/ se) —
     isse har plugin apne handlers client par attach kar leta hai.
  4. Bot run karta hai jab tak stop na ho.
"""

from pyrogram import Client

import config
from Mikasa.plugins import broadcast, logger, reply, start, stats

config.validate()

app = Client(
    "mikasa",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

# Har plugin apne handlers register karta hai
start.register(app)
reply.register(app)
broadcast.register(app)
stats.register(app)
logger.register(app)  # group add/remove tracking

if __name__ == "__main__":
    print("Mikasa Bot Running...")
    app.run()
