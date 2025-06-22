# Telegram Bot Template

A modern, structured Python template for building reliable and maintainable Telegram bots with [python-telegram-bot](https://docs.python-telegram-bot.org/).  
Supports modular design, asynchronous architecture, and production-ready deployment.

## 🚀 Features

- Full `asyncio` support
- Modular handler auto-discovery
- `@command` decorator for registering commands
- Supports command aliases
- `@admin_required` decorator for access control
- Global error handling
- MarkdownV2-safe output
- Rotating log files with level-based separation (errors, info, debug)
- Environment-based configuration using Pydantic
- Built-in unit tests for command registration
- Polling & webhook mode support
- GitHub Actions CI workflow

## 📦 Requirements

- Python 3.11+
- `python-telegram-bot==22.1` – main Telegram Bot API framework
- `aiohttp==3.12` – async HTTP server for webhooks
- `pydantic==2.11.7` – runtime data validation and settings
- `pydantic-settings==2.9.1` – environment-based settings loader

## ⚙️ Setup

```bash
git clone https://github.com/yourname/telegram-bot.git
cd telegram-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then edit it
```

## 🔐 Environment Variables

| Variable           | Description                                                             |
|--------------------|-------------------------------------------------------------------------|
| `BOT_TOKEN`        | Your bot token from BotFather                                           |
| `ADMIN_ID`         | Your Telegram user ID (int)                                             |
| `RUN_MODE`         | `polling` or `webhook`                                                  |
| `WEBHOOK_URL`      | Your public HTTPS endpoint                                              |
| `WEBHOOK_PORT`     | Port to listen on (e.g., 8443)                                          |
| `LOG_LEVEL`        | Log level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`          |
| `LOG_DIR`          | Directory where rotating log files will be saved                        |
| `LOG_BOT_FILE`     | Main rotating log file name (e.g. `bot.log`)                            |
| `LOG_ERRORS_FILE`  | Separate error log file name (e.g. `errors.log`)                        |

## ▶️ Run

**Development (polling):**
```bash
python main.py --mode polling
```

**Production (webhook):**
```bash
python main.py --mode webhook
```

## 📂 Project Structure

```
bot/
├── core/              # Startup and webhook runner
├── handlers/          # Modular command handlers
├── utils/             # Logging, env checks, Markdown formatter
├── config.py          # Loads environment into config
├── handlers_loader.py # Discovers and registers handlers
main.py                # Bot entrypoint
.env.example           # Example environment file
tests/                 # Basic tests
```

## 🧪 Testing

```bash
pytest
```

## 🖥️ Deployment

### `systemd` service
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
User=telegram
WorkingDirectory=/var/www/telegram-bot
ExecStart=/var/www/telegram-bot/venv/bin/python3 main.py --mode webhook
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Nginx Reverse Proxy
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate     /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /webhook {
        proxy_pass         http://127.0.0.1:8443/;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
}
```

## 📄 License

MIT License
