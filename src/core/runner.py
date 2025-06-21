"""Core bot runner module.

Initializes the Telegram bot application with all handlers, error processing,
and startup mode (polling or webhook). Provides entry points for bot execution
and integrates logging, command registration, and graceful exception handling.
"""

import asyncio

from telegram.ext import Application, ApplicationBuilder, MessageHandler, filters

from src.config import settings
from src.core.error_handler import handle_error
from src.handlers.fallback import unknown_command
from src.handlers_loader import register_handlers
from src.utils.commands import make_set_commands
from src.utils.logger import logger


async def _shutdown_app() -> None:
    """Provide graceful shutdown logic if needed."""
    await asyncio.sleep(0)  # No-op for now


def create_application() -> Application:
    """Build and configure the Telegram bot application."""
    app = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    logger.debug("✅ Application built")
    register_handlers(app)
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    app.post_init = make_set_commands()
    app.post_shutdown = _shutdown_app
    app.add_error_handler(handle_error)
    return app


def start_webhook(app: Application) -> None:
    """Start webhook server with Application.run_webhook()."""
    logger.info("🚀 Launching webhook listener")
    logger.info(
        "🌍 Listening on: http://%s:%s",
        settings.WEBHOOK_LISTEN,
        settings.WEBHOOK_PORT,
    )
    logger.info("🔗 Webhook URL: %s", settings.WEBHOOK_URL)

    app.run_webhook(
        listen=settings.WEBHOOK_LISTEN,
        port=settings.WEBHOOK_PORT,
        webhook_url=settings.WEBHOOK_URL,
    )


def run_webhook() -> None:
    """Build the bot application and run it in webhook mode."""
    app = create_application()
    start_webhook(app)


def start_polling(app: Application) -> None:
    """Start the bot using Application.run_polling."""
    logger.info("🚀 Launching polling mode")
    app.run_polling()


def run_polling() -> None:
    """Build the bot application and run it in polling mode."""
    app = create_application()
    start_polling(app)


def run_telegram_bot(mode: str = settings.RUN_MODE) -> None:
    """Entry point to run the bot in polling or webhook mode."""
    try:
        if mode == "polling":
            run_polling()
        else:
            run_webhook()
    except (OSError, RuntimeError) as e:
        logger.exception("🚨 Bot failed to start: %s", e)
        import time

        logger.info("⏳ Waiting 5 seconds before exit to avoid restart loop...")
        time.sleep(5)
