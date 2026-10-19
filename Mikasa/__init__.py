import importlib

from pyrogram import Client

import config
from Mikasa.plugins import all_modules

config.validate()

app = Client(
    "mikasa",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

for _module in all_modules:
    importlib.import_module(f"Mikasa.plugins.{_module}")
