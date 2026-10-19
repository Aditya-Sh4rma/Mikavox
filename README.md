# Mikasa

Mikasa is a Telegram auto-reply bot built for Burmese group chats. It handles
keyword replies, random replies, premium emoji, stickers, link cleanup,
broadcasts and a small sudo system. It runs on Python and MongoDB and is meant
to run as a worker process, not a web service.

No dashboard, no Redis, no extra services. Just a bot process and a database.

## What it does

- Answers greetings and small talk using keys from `prm_replies.json`
- Sends a random reply from `replies.json` when someone mentions `mikasa` or replies to the bot
- Adds premium emoji tags to replies
- Replies with a random sticker when someone sends a sticker to the bot
- Drops an emoji in groups every 20 to 30 messages
- Deletes links from non-admins and posts a warning with a Close button
- Stores users, groups and sudo users in MongoDB
- Broadcasts messages to groups and users with flags
- Sends a `Bot started` notice to the log group on every startup
- Loads every plugin inside `Mikasa/plugins` automatically

## Requirements

- Python 3.10 or newer
- MongoDB Atlas account
- API ID and API hash from my.telegram.org
- Bot token from @BotFather

## Quick start

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

When the configuration is valid you will see `Bot started`. Stop it
with `Ctrl+C`.

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `API_ID` | Yes | Telegram API ID |
| `API_HASH` | Yes | Telegram API hash |
| `BOT_TOKEN` | Yes | Bot token from @BotFather |
| `MONGO_URL` | Yes | MongoDB connection string |
| `OWNER_ID` | Yes | Telegram ID of the owner |
| `LOG_GROUP_ID` | No | Group for start and join logs |
| `OWNER_USERNAME` | No | Username used on the start button |
| `SUPPORT_CHAT` | No | Support link on the start button |
| `SUPPORT_CHANNEL` | No | Updates link on the start button |
| `START_IMAGE` | No | Image URL or file ID for the start message |

`OWNER_ID` is required. The bot exits during startup if it is missing. The
owner can add sudo users with `/addsudo`; those users then get access to the
owner-level commands.

The current defaults for the support and owner links are already set in
`config.py`, so the start buttons work even if those variables are empty.

## Telegram setup

1. Open my.telegram.org and create an application to get `API_ID` and `API_HASH`.
2. Open @BotFather, send `/newbot` and copy the token into `BOT_TOKEN`.
3. Send `/setprivacy` to @BotFather, select the bot and choose Disable.
4. Create a log group, add the bot and promote it to administrator.
5. Set the log group ID as `LOG_GROUP_ID`.

Privacy mode must be disabled for group add and remove logs.

## MongoDB setup

1. Create a free cluster on cloud.mongodb.com.
2. Create a database user with read and write access.
3. Allow `0.0.0.0/0` or your server IP in Network Access.
4. Open Connect, choose Drivers and copy the connection string.
5. Replace the password placeholder and use the result as `MONGO_URL`.

The bot creates the `mikasa` database and collections on first use. You do not
need to create anything by hand.

## Running on a VPS with systemd

This is the recommended setup if the bot should stay online.

Install the packages:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

Create a user and directory for the bot:

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

Add the environment file:

```bash
sudo -u mikasa cp .env.example .env
sudo -u mikasa nano .env
```

Do one manual run before creating the service:

```bash
sudo -u mikasa venv/bin/python main.py
```

Stop it once `Bot started` appears, then create the unit file:

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

Enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mikasa
sudo systemctl start mikasa
```

Check it:

```bash
sudo systemctl status mikasa
sudo journalctl -u mikasa -f
```

Update later:

```bash
cd /opt/mikasa
sudo -u mikasa git pull
sudo -u mikasa venv/bin/pip install -r requirements.txt
sudo systemctl restart mikasa
```

Run only one instance. Two instances cause a
`Conflict: terminated by other getUpdates request` error.

## Running on a VPS with tmux

tmux is fine for a quick setup. It will not start again after a reboot, so this
is not ideal for long-term hosting.

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

Detach with `Ctrl+B`, then `D`. The process keeps running in the background.

```bash
tmux attach -t mikasa
tmux ls
tmux kill-session -t mikasa
```

After a reboot, create the session again and start the bot.

## Running on Heroku

Heroku no longer has a free tier, but the included `Procfile` works.

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

Do not upload `.env`. Set every value with `heroku config:set`. The bot runs as
a worker dyno, so a web dyno is not needed.

## Commands

| Command | Who | Description |
|---|---|---|
| `/start` | Everyone | Saves the user or group and shows the start message |
| `/stats` | Owner or sudo | Shows total users and groups. Others are ignored |
| `/addsudo <reply/@user/id>` | Owner | Adds a sudo user |
| `/delsudo <reply/@user/id>` | Owner | Removes a sudo user |
| `/listsudo` | Owner or sudo | Lists the owner and sudo users |
| `/broadcast` | Owner or sudo | Sends a message to groups or users |

Aliases: `/rmsudo` and `/sudolist`.

## Broadcast

```text
/broadcast <text>
/broadcast              reply to any message
```

| Flag | Effect |
|---|---|
| `-user` | Also sends to saved users |
| `-nochat` | Skips groups |
| `-copy` | Copies instead of forwarding |

Examples:

```text
/broadcast -user -copy
/broadcast -nochat -user Hello everyone
```

Groups are the default target. Failed targets are written to
`broadcast_errors.txt` and sent back to the person who ran the command.

## Customising

### Replies

`replies.json` is a list:

```json
["reply one", "reply two", "reply three"]
```

`prm_replies.json` maps keywords to reply lists:

```json
{
  "hi": ["Hello", "Hey", "Hi there"],
  "bye": ["Bye", "See you"]
}
```

Both files are cached at startup. Restart the bot after editing them.

### Premium emojis

Add emoji IDs to `PREMIUM_EMOJIS` in `Mikasa/emoji.py`:

```python
PREMIUM_EMOJIS = {
    "any emoji": "5771840969515208083",
}
```

The dictionary can stay empty. Replies will be sent without premium tags.

### Stickers

Add sticker file IDs to `STICKERS` in `Mikasa/sticker.py`. The bot picks one at
random when someone replies to it with a sticker.

## Troubleshooting

| Problem | Check |
|---|---|
| `Missing required env vars` | The environment file is incomplete |
| Bot does not reply in groups | Privacy mode is still enabled in @BotFather |
| No start or group logs | The bot is not in the log group or not an admin |
| MongoDB connection error | Password or Network Access settings |
| `Conflict: terminated by other getUpdates request` | A second instance is running |
| `database is locked` | Two instances share the same session file |
| `pyrogram.enums has no ButtonStyle` | The wrong fork is installed, run `pip install -r requirements.txt` |
| Broadcast stops halfway | Telegram flood limit, wait and try again |

## Contributing

Fork the repo, make a branch, change what you need and open a pull request. Keep
the code small and the messages in English.

```bash
git checkout -b feature/something
git commit -m "Add something useful"
git push origin feature/something
```

## Support

Support chat: [SamuraisSupport](https://t.me/SamuraisSupport)

Owner: [@itz_m4rvin](https://t.me/itz_m4rvin)

If something breaks, include the command you ran and the error from the logs.
It makes debugging much faster.

## License

MIT. See `LICENSE` for the full text.

If this bot saved you some time, a star on the repository is appreciated:
[Aditya-Sh4rma/mikchat](https://github.com/Aditya-Sh4rma/mikchat).
