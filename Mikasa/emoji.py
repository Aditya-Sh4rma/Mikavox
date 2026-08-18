"""
Mikasa/emoji.py
Premium (custom) emoji ki list yahan rakhni hai.

Format: normal emoji -> uski custom_emoji_id (Telegram Premium se milti hai)
    PREMIUM_EMOJIS = {
        "😊": "5368324170671202286",
        "🔥": "5368353098706048670",
        ...
    }

Kaise use hoga:
  - reply.py har default/smart reply ke aage ek random emoji chunega
  - get_random_emoji_html() us emoji ko Telegram ke <emoji> HTML tag mein
    convert karke deta hai, jo Pyrogram HTML parse_mode samajhta hai:
        <emoji id="5368324170671202286">😊</emoji>
  - Ye tag tabhi kaam karega jab bot ka OWNER account Telegram Premium
    hold karta ho — warna normal emoji fallback hoga.

Tumhe bas neeche wali PREMIUM_EMOJIS dictionary fill karni hai
kam se kam 100 entries ke saath. Baaki sab automatic hai.
"""

import random

# ⬇️ Yahan apni 100+ premium emoji entries daalo (emoji: "custom_emoji_id")
PREMIUM_EMOJIS: dict[str, str] = {
    # "😊": "5368324170671202286",
    # "🔥": "5368353098706048670",
}


def get_random_emoji_html() -> str:
    """Random premium emoji ka HTML tag return karta hai.
    Agar PREMIUM_EMOJIS khaali hai (abhi tak fill nahi hui), toh
    khaali string return karega — bot crash nahi hoga, emoji bas nahi lagega."""
    if not PREMIUM_EMOJIS:
        return ""

    emoji_char, emoji_id = random.choice(list(PREMIUM_EMOJIS.items()))
    return f'<emoji id="{emoji_id}">{emoji_char}</emoji>'
