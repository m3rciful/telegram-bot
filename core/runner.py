"""Core bot runner module.

Initializes the Telegram bot application with all handlers, error processing,
and startup mode (polling or webhook). Provides entry points for bot execution
and integrates logging, command registration, and graceful exception handling.
"""

from config import BOT_TOKEN, WEBHOOK_LISTEN, WEBHOOK_PORT, WEBHOOK_URL
from core.error_handler import handle_error
from handlers.fallback import unknown_command
from handlers_loader import register_handlers
from telegram.ext import Application, ApplicationBuilder, MessageHandler, filters
from utils.commands import make_set_commands
from utils.logger import logger


def create_application() -> Application:
    """Build and configure the Telegram bot application."""
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    logger.debug("✅ Application built")
    register_handlers(app)
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    app.post_init = make_set_commands()
    app.add_error_handler(handle_error)
    return app


def start_webhook(app: Application) -> None:
    """Start webhook server with Application.run_webhook()."""
    logger.info("🚀 Launching webhook listener")
    logger.info("🌍 Listening on: http://%s:%s", WEBHOOK_LISTEN, WEBHOOK_PORT)
    logger.info("🔗 Webhook URL: %s", WEBHOOK_URL)

    app.run_webhook(
        listen=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        webhook_url=WEBHOOK_URL,
    )


def run_webhook() -> None:
    """Build the bot application and run it in webhook mode."""
    app = create_application()
    start_webhook(app)


def run_telegram_bot() -> None:
    """Entry point to run the bot with webhook. Handles startup exceptions."""
    try:
        run_webhook()
    except (OSError, RuntimeError) as e:
        logger.exception("🚨 Bot failed to start: %s", e)
        import time
        logger.info("⏳ Waiting 5 seconds before exit to avoid restart loop...")
        time.sleep(5)
