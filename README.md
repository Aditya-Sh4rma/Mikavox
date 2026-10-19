<div align="center">

<h2>Mikasa</h2>

<b>A small Telegram auto-reply bot for Burmese chat groups</b><br>
Keyword replies, premium emojis, stickers, link filtering, broadcasts and a
MongoDB-backed sudo system.

<a href="https://github.com/Aditya-Sh4rma/mikchat/stargazers">
    <img src="https://img.shields.io/github/stars/Aditya-Sh4rma/mikchat?color=blueviolet&logo=github&logoColor=black&style=for-the-badge" alt="Stars"/>
</a>
<a href="https://github.com/Aditya-Sh4rma/mikchat/network/members">
    <img src="https://img.shields.io/github/forks/Aditya-Sh4rma/mikchat?color=blueviolet&logo=github&logoColor=black&style=for-the-badge" alt="Forks"/>
</a>
<a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Written%20in-Python-blue?style=for-the-badge&logo=python" alt="Python"/>
</a>
<a href="https://t.me/SamuraisSupport">
    <img src="https://img.shields.io/badge/Support-Telegram-blue?style=for-the-badge&logo=telegram" alt="Support"/>
</a>

</div>

<hr>

Mikasa is a Telegram bot I put together for a Burmese chat group. It sits in the
group, answers the usual greetings, drops a premium emoji now and then, replies
to stickers and keeps the place alive. It also has a link filter, a broadcast
system and a small sudo list so not everyone can spam the whole userbase.

There is no dashboard, no Redis, no Docker requirement. It is just Python, a
MongoDB database and a bot token. If you can run a Python script on a VPS, you
can run this.

<hr>

<h2>🔥 Features</h2>

- 💬 Keyword replies from `prm_replies.json`
- 🎲 Random replies from `replies.json` when someone mentions `mikasa` or replies to the bot
- 🪙 Premium emoji tags on replies
- 🧩 Random sticker replies
- 📈 Group activity counter that drops an emoji every 20 to 30 messages
- 🚫 Link filter for non-admins with an inline warning
- 👥 User, group and sudo tracking in MongoDB
- 📢 Broadcast with `-user`, `-nochat` and `-copy` flags
- 🎨 Colored inline buttons (blue actions, red close)
- 🛡️ Owner and sudo commands that survive restarts
- 🔌 Plugins load automatically from the `Mikasa/plugins` folder
- 📝 Start and group add/remove logs

<hr>

<h2>📁 What is inside</h2>

<details>
    <summary>Repository structure</summary>

```text
mikchat/
├── main.py                  # Entry point
├── config.py                # Environment variables and validation
├── replies.json             # Default reply pool
├── prm_replies.json         # Keyword based replies
├── smart_replies.json       # Reserved for later
├── requirements.txt
├── Procfile                 # Heroku worker
├── runtime.txt              # Heroku Python version
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── Mikasa/
    ├── __init__.py          # Client setup and plugin loading
    ├── mongo.py             # users, groups and sudoers
    ├── emoji.py             # Premium emoji IDs
    ├── sticker.py           # Sticker file IDs
    ├── sudo.py              # Sudo cache and permission filters
    ├── utils.py             # Small shared helpers
    └── plugins/
        ├── __init__.py      # Finds plugin modules
        ├── start.py         # /start
        ├── reply.py         # Auto replies, emojis and stickers
        ├── broadcast.py     # /broadcast and /stopbroadcast
        ├── sudoers.py       # /addsudo, /delsudo and /listsudo
        ├── linkfilter.py    # Deletes links from non-admins
        ├── logger.py        # Start and group logs
        └── stats.py         # /stats
```

Every file inside `Mikasa/plugins/` is imported on startup. If you add a new
plugin there, you do not need to touch `main.py`.
</details>

<hr>

<h2>⚙️ Configuration</h2>

Copy the example file and fill it in:

```bash
cp .env.example .env
nano .env
```

| Variable | Required | What it is |
|---|---|---|
| `API_ID` | Yes | From my.telegram.org |
| `API_HASH` | Yes | From my.telegram.org |
| `BOT_TOKEN` | Yes | From @BotFather |
| `MONGO_URL` | Yes | MongoDB Atlas connection string |
| `OWNER_ID` | Yes | Your Telegram user ID |
| `ADMIN_IDS` | No | Extra sudo users, comma separated |
| `LOG_GROUP_ID` | No | Group where start and join logs go |
| `OWNER_USERNAME` | No | Username on the start button |
| `SUPPORT_CHAT` | No | Support link on the start button |
| `SUPPORT_CHANNEL` | No | Updates link on the start button |
| `START_IMAGE` | No | Image URL or file ID for `/start` |

If `OWNER_ID` is missing, the first ID in `ADMIN_IDS` becomes the owner. At
least one of them has to be there, otherwise the bot exits on startup with a
clear message.

<details>
    <summary>Example .env</summary>

```env
API_ID=123456
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=123456:ABC-DEF1234567890
MONGO_URL=mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority
OWNER_ID=123456789
ADMIN_IDS=123456789
LOG_GROUP_ID=-1001234567890
OWNER_USERNAME=itz_m4rvin
SUPPORT_CHAT=https://t.me/SamuraisSupport
SUPPORT_CHANNEL=https://t.me/SamuraisSupport
START_IMAGE=
```
</details>

<hr>

<h2>☁️ Deployment</h2>

<h3>✔️ Before you start</h3>

- Python 3.10 or newer
- A MongoDB Atlas cluster and connection string
- `API_ID` and `API_HASH` from my.telegram.org
- A bot token from @BotFather
- Privacy mode disabled in @BotFather, otherwise group add/remove logs will not work

<details>
    <summary><h3>MongoDB Atlas</h3></summary>

1. Create a free cluster at cloud.mongodb.com.
2. Create a database user with read and write access.
3. In Network Access, allow `0.0.0.0/0` or your server IP.
4. Click Connect, choose Drivers and copy the connection string.
5. Replace the password placeholder and paste it into `MONGO_URL`.

The bot creates the `mikasa` database and its collections on its own. You do
not need to create them manually.
</details>

<details>
    <summary><h3>Local or quick VPS test</h3></summary>

```bash
git clone https://github.com/Aditya-Sh4rma/mikchat.git
cd mikchat

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env

python main.py
```

If the env values are fine, you will see `Mikasa Bot Running...`. Press `Ctrl+C`
to stop it.
</details>

<details>
    <summary><h3>VPS with systemd (recommended for 24/7)</h3></summary>

Install the basics:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

Create a separate user so the bot does not run as root:

```bash
sudo useradd -m -s /bin/bash mikasa
sudo mkdir -p /opt/mikasa
sudo chown mikasa:mikasa /opt/mikasa
```

Clone and install:

```bash
sudo -u mikasa git clone https://github.com/Aditya-Sh4rma/mikchat.git /opt/mikasa
cd /opt/mikasa

sudo -u mikasa python3 -m venv venv
sudo -u mikasa venv/bin/pip install --upgrade pip
sudo -u mikasa venv/bin/pip install -r requirements.txt
```

Add your values:

```bash
sudo -u mikasa cp .env.example .env
sudo -u mikasa nano .env
```

Do one manual run before creating the service:

```bash
sudo -u mikasa venv/bin/python main.py
```

Stop it after `Mikasa Bot Running...` appears.

Create the service:

```bash
sudo nano /etc/systemd/system/mikasa.service
```

Paste this:

```ini
[Unit]
Description=Mikasa Telegram Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=mikasa
WorkingDirectory=/opt/mikasa
EnvironmentFile=/opt/mikasa/.env
ExecStart=/opt/mikasa/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mikasa
sudo systemctl start mikasa
```

Useful commands:

```bash
sudo systemctl status mikasa
sudo journalctl -u mikasa -f
sudo systemctl restart mikasa
sudo systemctl stop mikasa
```

Updating later:

```bash
cd /opt/mikasa
sudo -u mikasa git pull
sudo -u mikasa venv/bin/pip install -r requirements.txt
sudo systemctl restart mikasa
```

Keep only one copy running. Two instances will fight over Telegram updates and
you will see `Conflict: terminated by other getUpdates request`.
</details>

<details>
    <summary><h3>VPS with tmux (simple, no service)</h3></summary>

tmux is fine if you just want the bot running without setting up systemd. It
will not restart itself after a reboot, so keep that in mind.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git tmux

git clone https://github.com/Aditya-Sh4rma/mikchat.git
cd mikchat

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env

tmux new -s mikasa
source venv/bin/activate
python main.py
```

Detach from tmux with `Ctrl+B`, then `D`. The bot keeps running.

```bash
tmux attach -t mikasa
tmux ls
tmux kill-session -t mikasa
```

If the server reboots, start the session and run `python main.py` again. For a
permanent setup, use the systemd option above.
</details>

<details>
    <summary><h3>Heroku</h3></summary>

Heroku does not have a free tier anymore, but the included `Procfile` is ready.

```bash
heroku login
heroku create your-app-name

heroku config:set API_ID=123456
heroku config:set API_HASH=your_api_hash
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set MONGO_URL=your_mongo_url
heroku config:set OWNER_ID=123456789
heroku config:set LOG_GROUP_ID=-1001234567890

git push heroku main
heroku ps:scale worker=1
heroku logs --tail
```

Do not push `.env` to Heroku. Use `heroku config:set` for every value. The bot
runs as a worker dyno, so no web dyno is needed.
</details>

<hr>

<h2>🧐 Usage</h2>

1. Add the bot to your group.
2. Promote it to admin if you want the link filter and logs to work properly.
3. Send `/start` in private to make sure everything is wired up.
4. Use `/start` in the group once so the group gets saved to MongoDB.

<details>
    <summary>Commands</summary>

| Command | Who | What it does |
|---|---|---|
| `/start` | Everyone | Shows the start message and saves the user or group |
| `/stats` | Everyone | Shows total users and groups |
| `/addsudo <reply/@user/id>` | Owner | Adds a sudo user |
| `/delsudo <reply/@user/id>` | Owner | Removes a sudo user |
| `/listsudo` | Owner or sudo | Shows the owner and sudo users |
| `/broadcast` | Owner or sudo | Sends a message to groups or users |
| `/stopbroadcast` | Owner or sudo | Stops a running broadcast |

Aliases: `/rmsudo` for `/delsudo`, `/sudolist` for `/listsudo`,
`/stop_gcast` for `/stopbroadcast`.

</details>

<details>
    <summary>Broadcast flags</summary>

```text
/broadcast <text>
/broadcast              reply to any message
```

| Flag | What it does |
|---|---|
| `-user` | Also sends to saved users. Without it only groups are targeted |
| `-nochat` | Skips groups |
| `-copy` | Copies the message instead of forwarding it |

Examples:

```text
/broadcast -user -copy
/broadcast -nochat -user Hello everyone
```

Failed targets are written to `broadcast_errors.txt` and sent back to the
person who started the broadcast.
</details>

<details>
    <summary>Automatic behaviour</summary>

- Any text that matches a key in `prm_replies.json` gets a random reply from that key.
- Messages containing `mikasa` or replies to the bot get a random reply from `replies.json`.
- Stickers sent as a reply to the bot get a random sticker back.
- Groups get a premium emoji every 20 to 30 messages.
- Links from non-admins are deleted and replaced with a warning and a Close button.
- Sudo users and group admins are not affected by the link filter.
</details>

<hr>

<h2>🛠️ Customising</h2>

<details>
    <summary>Replies</summary>

`replies.json` is a plain list:

```json
["reply one", "reply two", "reply three"]
```

`prm_replies.json` maps keywords to lists:

```json
{
  "hi": ["Hello", "Hey", "Hi there"],
  "bye": ["Bye", "See you"]
}
```

Both files are cached when the bot starts. Restart after editing them.
</details>

<details>
    <summary>Premium emojis</summary>

Open `Mikasa/emoji.py` and add entries to `PREMIUM_EMOJIS`:

```python
PREMIUM_EMOJIS = {
    "😭": "5771840969515208083",
}
```

Leave the dictionary empty if you do not have premium emoji IDs. The bot will
work without them.
</details>

<details>
    <summary>Stickers</summary>

Add sticker file IDs to `STICKERS` in `Mikasa/sticker.py`. One per line. The
bot picks a random one when someone replies to it with a sticker.
</details>

<hr>

<h2>🐛 Troubleshooting</h2>

| Problem | What to check |
|---|---|
| `Missing required env vars` | `.env` or dashboard variables are incomplete |
| Bot does not reply in groups | Privacy mode in @BotFather still enabled |
| No start or group logs | Bot is not in `LOG_GROUP_ID` or not admin there |
| MongoDB connection error | Wrong password or IP not allowed in Atlas |
| `Conflict: terminated by other getUpdates request` | Another instance is running |
| `database is locked` | Two instances share the same session file |
| Broadcast stops halfway | Telegram flood limit, wait and run it again |

<hr>

<h2>❤️ Contributing</h2>

If you want to change something, fork it and open a pull request. Keep the code
simple, keep the messages in English and do not add a hundred log lines. This
project is intentionally small.

1. Fork the repository.
2. Create a branch: `git checkout -b feature/something`.
3. Make your changes and test them.
4. Commit: `git commit -m "Add something useful"`.
5. Push: `git push origin feature/something`.
6. Open a pull request.

<hr>

<h2>📄 License</h2>

MIT. See the `LICENSE` file for the boring part.

<hr>

<h2>👀 Acknowledgements</h2>

- Thanks to the Pyrofork and Pyrogram maintainers.
- Thanks to everyone who reports bugs and sends fixes.
- Built and maintained by [@itz_m4rvin](https://t.me/itz_m4rvin).

<hr>

<div align="center">

If this bot saved you an evening of work, drop a star on the repo. It costs
nothing, and it makes the project easier to find.

⭐ <a href="https://github.com/Aditya-Sh4rma/mikchat"><b>Star Mikasa on GitHub</b></a>

<br><br>

<h2>🤞 Support</h2>

Something broken? Ask in the support chat or message the owner directly.
Include your logs and the command you ran, otherwise it is hard to help.

<a href="https://t.me/SamuraisSupport">
    <img src="https://img.shields.io/badge/Support%20Chat-Join%20Now-blue?style=for-the-badge&logo=telegram" alt="Support Chat"/>
</a>
<a href="https://t.me/itz_m4rvin">
    <img src="https://img.shields.io/badge/Owner-%40itz__m4rvin-blueviolet?style=for-the-badge&logo=telegram" alt="Owner"/>
</a>

<br><br>

Support chat: [@SamuraisSupport](https://t.me/SamuraisSupport)<br>
Owner: [@itz_m4rvin](https://t.me/itz_m4rvin)

</div>
