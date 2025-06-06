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

 📄 You can use the provided `.env.example` file as a starting point by renaming it to `.env` and updating the values.

5. Start the bot (for development):
   ```bash
   python main.py
   ```

# Or run as a webhook listener (recommended for production)
python main.py

## Production

This bot now uses the `Application.run_webhook()` method introduced in PTB 20+ for production. The webhook listener is built into the bot and should be proxied with a reverse proxy (e.g., Nginx). A `systemd` service handles automatic startup and recovery.

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
