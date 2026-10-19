# Mikasa

Mikasa is a Telegram auto-reply bot for Burmese group chats. It replies to
messages, sends premium emojis and stickers, removes links, and can broadcast
to groups and users. Built with Python and MongoDB.

## What it does

- Replies to greetings and small talk using `prm_replies.json`
- Sends a random reply from `replies.json` when someone mentions `mikasa` or replies to the bot
- Sends premium emoji tags and a random sticker for sticker replies
- Drops a random emoji in groups every 20 to 30 messages
- Deletes links posted by non-admins and replies with a Close button
- Stores users, groups and sudo users in MongoDB
- Broadcasts to groups and users with flags

## Requirements

- Python 3.10 or newer
- MongoDB Atlas account
- API ID and API hash from my.telegram.org
- Bot token from @BotFather

## Installation

Update the server and install the packages:

```bash
apt update && apt upgrade -y
apt install -y python3 python3-venv python3-pip git tmux
```

Clone the bot and install the packages:

```bash
git clone https://github.com/Aditya-Sh4rma/Mikavox.git
cd Mikavox

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Fill the environment file:

```bash
cp .env.example .env
nano .env
```

Start the bot:

```bash
python main.py
```

You will see `Bot started`. Stop it with `Ctrl+C`.

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

The owner can give access to more users with `/addsudo`.

## Telegram setup

1. Create an application on my.telegram.org to get `API_ID` and `API_HASH`.
2. Send `/newbot` to @BotFather and copy the token into `BOT_TOKEN`.
3. Send `/setprivacy` to @BotFather, select the bot and choose Disable.
4. Create a log group, add the bot and promote it to admin.
5. Set the group ID as `LOG_GROUP_ID`.

## MongoDB setup

1. Create a free cluster on cloud.mongodb.com.
2. Create a database user with read and write access.
3. Allow your IP, or `0.0.0.0/0`, in Network Access.
4. Copy the connection string from Connect, choose Drivers, and use it as `MONGO_URL`.

Collections are created automatically on the first run.

## Run with systemd

Create the service file:

```bash
nano /etc/systemd/system/mikasa.service
```

Paste this:

```ini
[Unit]
Description=Mikasa Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/Mikavox
ExecStart=/root/Mikavox/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start it:

```bash
systemctl daemon-reload
systemctl enable mikasa
systemctl start mikasa
```

Check the status and logs:

```bash
systemctl status mikasa
journalctl -u mikasa -f
```

Update later:

```bash
cd /root/Mikavox
git pull
venv/bin/pip install -r requirements.txt
systemctl restart mikasa
```

Run only one instance, otherwise Telegram throws a
`Conflict: terminated by other getUpdates request` error.

## Run with tmux

```bash
tmux new -s mikasa
source venv/bin/activate
python main.py
```

Detach with `Ctrl+B` then `D`.

```bash
tmux attach -t mikasa
tmux kill-session -t mikasa
```

tmux does not survive a reboot, so the bot has to be started again after one.

## Run on Heroku

```bash
heroku login
heroku create your-app-name
heroku config:set API_ID=123456 API_HASH=your_api_hash BOT_TOKEN=your_bot_token
heroku config:set MONGO_URL=your_mongo_url OWNER_ID=123456789 LOG_GROUP_ID=-1001234567890

git push heroku main
heroku ps:scale worker=1
heroku logs --tail
```

The bot runs as a worker dyno, no web dyno is needed.

## Commands

| Command | Who | Description |
|---|---|---|
| `/start` | Everyone | Saves the user or group |
| `/stats` | Owner or sudo | Shows total users and groups |
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

Groups are sent by default. Example:

```text
/broadcast -user -copy
```

Failed targets are written to `broadcast_errors.txt` and sent back to the
sender.

## Customising

### Replies

`replies.json` is a list of strings:

```json
["reply one", "reply two"]
```

`prm_replies.json` maps keywords to replies:

```json
{
  "hi": ["Hello", "Hey"],
  "bye": ["Bye", "See you"]
}
```

Restart the bot after editing either file.

### Premium emojis

Add emoji IDs to `PREMIUM_EMOJIS` in `Mikasa/emoji.py`:

```python
PREMIUM_EMOJIS = {
    "any emoji": "5771840969515208083",
}
```

Leave it empty to send replies without premium tags.

### Stickers

Add sticker file IDs to `STICKERS` in `Mikasa/sticker.py`.

## Troubleshooting

| Problem | Check |
|---|---|
| `Missing required env vars` | The environment file is incomplete |
| Bot does not reply in groups | Privacy mode is still enabled in @BotFather |
| No logs in the log group | The bot is not in the group or not an admin |
| MongoDB connection error | Password or Network Access settings |
| `Conflict: terminated by other getUpdates request` | A second instance is running |
| `database is locked` | Two instances share the same session file |
| `pyrogram.enums has no ButtonStyle` | Run `pip install -r requirements.txt` |
| Broadcast stops halfway | Telegram flood limit, wait and try again |

## Contributing

Fork the repo, make your changes and open a pull request. Keep the code small
and the messages in English.

## Support

Support chat: [SamuraisSupport](https://t.me/SamuraisSupport)
Owner: [@itz_m4rvin](https://t.me/itz_m4rvin)

## License

MIT, see `LICENSE`.

If this bot saved you some time, a star on the repo is appreciated:
[Aditya-Sh4rma/Mikavox](https://github.com/Aditya-Sh4rma/Mikavox).
