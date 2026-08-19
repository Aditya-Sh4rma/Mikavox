import random

# Apne sticker file_id yahan daalo (Telegram se sticker forward karke @userinfobot
# ya @RawDataBot ko bhejo, wahan se "file_id" copy karo).
# Kam se kam 100 ID daalne hain — jitni zyada honge utna variety milega.
STICKERS: list[str] = [
    "CAACAgUAAxkBAAEBAAABAAABAAABAAABAAABAAABAAAB",  # placeholder 1
    "CAACAgUAAxkBAAEBAAABAAABAAABAAABAAABAAABAAAC",  # placeholder 2
    "CAACAgUAAxkBAAEBAAABAAABAAABAAABAAABAAABAAAD",  # placeholder 3
    # ... tum apne 100+ sticker file_id yahan add karte jao
]


def get_random_sticker() -> str | None:
    if not STICKERS:
        return None
    return random.choice(STICKERS)
