"""Core bot runner module.

Initializes the Telegram bot application with all handlers, error processing,
and startup mode (polling or webhook). Provides entry points for bot execution
and integrates logging, command registration, and graceful exception handling.
"""
import asyncio
import socket

from aiohttp import web
from config import BOT_TOKEN, WEBHOOK_PORT, WEBHOOK_URL
from handlers.fallback import unknown_command
from handlers_loader import register_handlers
from telegram.ext import Application, ApplicationBuilder, MessageHandler, filters
from utils.commands import make_set_commands
from utils.error_handler import handle_error
from utils.logger import logger
from webhook_server import create_webhook_app


def create_application() -> Application:
    """Build and configure the Telegram bot application."""
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    logger.debug("✅ Application built")
    register_handlers(app)
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    app.post_init = make_set_commands()
    app.add_error_handler(handle_error)
    return app


async def run_webhook() -> None:
    """Start the bot in webhook mode, binding to the configured port."""
    app = create_application()

    def is_port_in_use(port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("127.0.0.1", port)) == 0

    if is_port_in_use(WEBHOOK_PORT):
        logger.error(
            "❌ Port %s is already in use. Aborting webhook startup.",
            WEBHOOK_PORT
        )
        return

    web_app = create_webhook_app(app)
    await app.initialize()
    await app.bot.set_webhook(WEBHOOK_URL)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", WEBHOOK_PORT)
    logger.info("🌐 Starting webhook on http://0.0.0.0:%s", WEBHOOK_PORT)
    await site.start()
    await asyncio.Event().wait()


def run_bot() -> None:
    """Entry point to run the bot with webhook. Handles startup exceptions."""
    try:
        asyncio.run(run_webhook())
    except RuntimeError as e:
        logger.exception("🚨 Bot failed to start: %s", e)
