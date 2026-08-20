import random

STICKERS: list[str] = [
    "CAACAgUAAyEFAATr9eOrAAIUUmqF3LIiSGIIuRoDRZK2iFMJ2utqAAKRGwAC56ApVfKMIZOq0cN0PQQ",
]


def get_random_sticker() -> str | None:
    if not STICKERS:
        return None
    return random.choice(STICKERS)
