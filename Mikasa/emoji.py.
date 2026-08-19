import random

PREMIUM_EMOJIS: dict[str, str] = {
    "😭": "5771840969515208083",
}


def get_random_emoji_html() -> str:
    if not PREMIUM_EMOJIS:
        return ""

    emoji_char, emoji_id = random.choice(list(PREMIUM_EMOJIS.items()))
    return f'<emoji id="{emoji_id}">{emoji_char}</emoji>'
