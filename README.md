# Telegram Bot Template

This project is a boilerplate for building Telegram bots using the [python-telegram-bot](https://docs.python-telegram-bot.org/) library.

## Features

- Asynchronous support with `asyncio`
- Webhook-based updates (no polling)
- Modular handler structure
- Logging system with rotation
- Environment-based configuration
- MarkdownV2-safe output formatting

## Requirements

- Python 3.11+
- `python-telegram-bot` v22.1
- `aiohttp`
- `python-dotenv`

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

5. Start the bot (for development):
   ```bash
   python main.py
   ```

## Production

This bot is designed to run via webhook. Use a reverse proxy (e.g., Nginx) and a systemd service for deployment. Make sure to set the required environment variables in `.env`.

## Project Structure

```
telegram_bot/
├── core/              # Main startup and webhook logic
├── handlers/          # Bot command handlers
├── utils/             # Utility modules (markdown, logger, etc.)
├── .env.example       # Example environment file
└── main.py            # Entrypoint for launching the bot
```

## License

MIT License
