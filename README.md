## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Production](#production)
- [Project Structure](#project-structure)
- [License](#license)

# Telegram Bot Template

This project is a boilerplate for building Telegram bots using the [python-telegram-bot](https://docs.python-telegram-bot.org/) library.

A clean, scalable, and production-ready Python template for building Telegram bots using the python-telegram-bot library.  
Ideal for developers looking to use async handlers, webhook-based updates, and modular design out of the box.

## Features

- Asynchronous support with `asyncio`
- Webhook-based updates (no polling)
- Modular handler structure
- Logging system with rotation
- Environment-based configuration
- MarkdownV2-safe output formatting

## Requirements

- Python 3.11+
- `python-telegram-bot==22.1`
- `python-dotenv==1.1.0`
- `colorama==0.4.6`
- `aiohttp==3.12`

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/m3rciful/telegram-bot.git
   cd telegram-bot
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example environment file and configure it:
   ```bash
   cp .env.example .env
   ```

 You can use the provided `.env.example` file as a starting point by renaming it to `.env` and updating the values.

### Environment Variables

- `BOT_TOKEN`: Your bot’s token from BotFather.
- `WEBHOOK_URL`: Public HTTPS URL that Telegram will call. Example: `https://yourdomain.com/webhook`
- `WEBHOOK_LISTEN`: Local address to bind the webhook server to (usually `0.0.0.0`).
- `WEBHOOK_PORT`: Port to listen on, e.g. `8443`.
- `LOG_LEVEL`: Logging level (`DEBUG`, `INFO`, `WARNING`, etc.).
- `LOG_DIR`: Directory for log files.
- `LOG_BOT_FILE`: Filename for general bot logs.
- `LOG_ERRORS_FILE`: Filename for error logs.
- `ADMIN_ID`: Telegram user ID with admin rights.
- `RUN_MODE`: `polling` for development or `webhook` for production.

You can also set the `RUN_MODE` environment variable instead of using
the `--mode` command-line option.

Use the optional `--diagnostics` flag to log environment information at startup.

5. Start the bot in polling mode (development):
   ```bash
   python main.py --mode polling
   ```

   Or run as a webhook listener (recommended for production):

   ```bash
   python main.py --mode webhook
   ```

Add `--diagnostics` to either command to include startup environment logs.

## Production

This bot now uses the `Application.run_webhook()` method introduced in PTB 20+ for production. The webhook listener is built into the bot and should be proxied with a reverse proxy (e.g., Nginx). A `systemd` service handles automatic startup and recovery.

### Example systemd Service Unit

```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
User=telegram
WorkingDirectory=/var/www/telegram/data/telegram_bot
ExecStart=/var/www/telegram/data/telegram_bot/venv/bin/python3 main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Basic Nginx Reverse Proxy Configuration

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate     /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /webhook {
        proxy_pass         http://127.0.0.1:8443/webhook;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
}
```

## Project Structure

```
telegram_bot/
├── core/              # Startup logic and webhook runner
├── handlers/          # Modular command handlers
├── services/          # External API or service integrations
├── utils/             # Utilities (env check, logging, markdown)
├── config.py          # Centralized config from environment
├── handlers_loader.py # Dynamic handler registration
├── main.py            # Entrypoint for bot startup
├── .env.example       # Example environment file
├── requirements.txt   # Python dependencies
└── README.md
```

## Dynamic Handler Registration

`handlers_loader.register_handlers` imports every module in the `handlers`
package. When a module is imported, any functions decorated with
`@command` from `utils.commands` are executed and stored in
`COMMAND_REGISTRY`. After all modules are loaded, the function iterates over
that registry and adds a `CommandHandler` for each command.

Modules may also define a `__callbacks__` dictionary mapping callback function
names to a dictionary of metadata (such as a regex `pattern`). These are used to
register `CallbackQueryHandler`s automatically.

Use the decorator like this:

```python
from utils.commands import command

@command("Description")
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ...
```

Callback query handlers can be declared inside the same module:

```python
__callbacks__ = {
    "button_callback": {"pattern": r"^btn:"}
}
```

## Testing

Run the test suite with [pytest](https://pytest.org/):

```bash
pytest
```


## License

MIT License
