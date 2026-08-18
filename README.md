# Mikasa

Telegram auto-reply bot (Burmese), Pyrofork + MongoDB Atlas par bana hua.

## Structure

```
.
├── main.py                  # Entry point (root)
├── config.py                 # Sab env vars yahan se load hote hain (root)
├── replies.json               # Default replies (khaali — khud fill karo)
├── smart_replies.json          # Keyword-based replies (khaali — khud fill karo)
├── requirements.txt
├── Procfile
├── runtime.txt
├── .env.example
├── .gitignore
├── README.md
└── Mikasa/
    ├── mongo.py               # Database (users, groups)
    ├── emoji.py                # Premium emoji list (khud fill karo)
    └── plugins/
        ├── __init__.py
        ├── start.py               # /start (private + group)
        ├── reply.py                # Auto-reply system
        ├── broadcast.py             # /broadcast (admin only)
        ├── logger.py                 # start / group-add / group-remove logs
        └── stats.py                   # /stats
```

## Local Setup

1. `.env.example` ko copy karke `.env` banao:
   ```
   cp .env.example .env
   ```
2. `.env` mein apni values bharo — `API_ID`, `API_HASH`, `BOT_TOKEN` (my.telegram.org
   aur @BotFather se), `MONGO_URL` (MongoDB Atlas se), `LOG_GROUP_ID`, `ADMIN_IDS`, etc.
3. Dependencies install karo:
   ```
   pip install -r requirements.txt
   ```
4. Bot chalao:
   ```
   python main.py
   ```

## replies.json aur smart_replies.json fill karna

Dono root mein hain (`Mikasa/` folder ke bahar).

- `replies.json` ek simple list hai:
  ```json
  ["reply 1", "reply 2", "reply 3"]
  ```
- `smart_replies.json` keyword -> replies mapping hai:
  ```json
  {
    "hi": ["Hi 👋", "Hello!"],
    "bye": ["Bye 👋"]
  }
  ```
- Dono files startup par cache ho jaati hain — bot chalte waqt baar baar
  disk se nahi padhi jaati, isliye fast rehta hai.

## Mikasa/emoji.py fill karna

`Mikasa/emoji.py` ke andar `PREMIUM_EMOJIS` dictionary mein apni premium
emoji ID's daalo (format file ke andar comment mein diya hai). Khaali
chhodne par bot normal chalega, bas emoji prefix nahi lagega.

## Heroku Deploy

1. Naya Heroku app banao aur is repo ko connect/push karo.
2. Heroku dashboard > Settings > Config Vars mein wahi sab variables daalo
   jo `.env.example` mein hain (asli values ke saath).
3. `Procfile` already `worker: python main.py` bola hua hai — Heroku dashboard
   mein **worker dyno ON** karna mat bhoolna (Resources tab), warna bot
   chalega hi nahi (default web dyno kaam nahi karega, ye worker hai).
4. Deploy hone ke baad logs check karo — agar koi env var missing hogi,
   `config.validate()` turant clear error dega.

## MongoDB Atlas

Free-tier cluster bana lo, "Connect your application" se connection string
lo, usme apna password daal ke `MONGO_URL` mein paste karo. Network Access
mein `0.0.0.0/0` allow karna hoga taaki Heroku se connect ho sake.

## BotFather privacy mode

`logger.py` mein group add/remove Pyrogram ke `ChatMemberUpdated` event se
detect hota hai — iske liye @BotFather mein bot ka **privacy mode OFF**
hona zaroori hai (`/setprivacy` -> Disable).
