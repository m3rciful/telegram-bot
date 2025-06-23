"""Core bot runner module.

Initializes the Telegram bot application with all handlers, error processing,
and startup mode (polling or webhook). Provides entry points for bot execution
and integrates logging, command registration, and graceful exception handling.
"""

import asyncio

from telegram.ext import Application, ApplicationBuilder, MessageHandler, filters

from bot.config import settings
from bot.core.error_handler import handle_error
from bot.handlers.fallback import unknown_command
from bot.handlers_loader import register_handlers
from bot.utils.commands import make_set_commands
from bot.utils.logger import logger


def create_application() -> Application:
    """Build and configure the Telegram bot application."""
    app = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    logger.info("✅ Application built")
    register_handlers(app)
    async def _post_init(app: Application) -> None:
        await make_set_commands()(app)

    app.post_init = _post_init
    app.post_shutdown = lambda app: _shutdown_app(app)
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    app.add_error_handler(handle_error)
    return app

async def _shutdown_app(_app: Application) -> None:
    """Graceful shutdown logic (e.g. close DB connections, clear caches)."""
    logger.info("🛑 Shutting down bot gracefully...")
    # Example: await some_db.disconnect()  # noqa: ERA001
    # Example: await some_cache.close()  # noqa: ERA001
    await asyncio.sleep(0)


def start_webhook(app: Application) -> None:
    """Start webhook server with Application.run_webhook()."""
    logger.debug("🚀 Launching webhook listener")
    logger.debug(
        "🌍 Listening on: http://%s:%s",
        settings.WEBHOOK_LISTEN,
        settings.WEBHOOK_PORT,
    )
    logger.debug("🔗 Webhook URL: %s", settings.WEBHOOK_URL)

    app.run_webhook(
        listen=settings.WEBHOOK_LISTEN,
        port=settings.WEBHOOK_PORT,
        webhook_url=settings.WEBHOOK_URL,
    )


def start_polling(app: Application) -> None:
    """Start the bot using Application.run_polling."""
    logger.debug("🚀 Launching polling mode")
    app.run_polling()


def run_telegram_bot(mode: str = settings.RUN_MODE) -> None:
    """Start the Telegram bot in the specified mode ('polling' or 'webhook')."""
    try:
        app = create_application()
        if mode == "polling":
            start_polling(app)
        else:
            start_webhook(app)
    except (OSError, RuntimeError, KeyboardInterrupt):
        logger.exception("🚨 Bot failed to start")
        import time
        logger.info("⏳ Waiting 5 seconds before exit to avoid restart loop...")
        time.sleep(5)
