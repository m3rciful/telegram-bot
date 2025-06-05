import logging
import sys

import aiohttp
from aiohttp import web
from config import WEBHOOK_PATH, WEBHOOK_PORT
from telegram import Update
from telegram.ext import Application

logger = logging.getLogger("webhook")


async def handle_webhook(request: web.Request) -> web.Response:
    """Handle incoming Telegram webhook update."""
    try:
        data = await request.json()
        logger.debug("Incoming webhook update: %s", data)
        peername = request.transport.get_extra_info("peername")
        if peername:
            logger.debug("Webhook request from IP: %s", peername[0])
        update = Update.de_json(data, request.app["telegram_app"].bot)
        await request.app["telegram_app"].process_update(update)
    except Exception:
        logger.exception("Failed to process update")
    return web.Response()


def add_webhook_routes(app: web.Application, telegram_app: Application) -> None:
    """Configure routes for webhook handler."""
    app["telegram_app"] = telegram_app
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    logger.debug("Web server routes set")
    logger.info("Starting webhook...")
    logger.debug("Running app.run_webhook with arguments:")
    logger.debug("listen=127.0.0.1, port=%s, path=%s", WEBHOOK_PORT, WEBHOOK_PATH)
    logger.info("Webhook listening on port %s, path=%s", WEBHOOK_PORT, WEBHOOK_PATH)


def create_webhook_app(telegram_app: Application) -> web.Application:
    """Create aiohttp web application with webhook routes."""
    logger.debug("Python executable: %s", sys.executable)
    app = web.Application()
    session = aiohttp.ClientSession()
    telegram_app.bot_data["session"] = session
    app["session"] = session
    add_webhook_routes(app, telegram_app)
    app.on_shutdown.append(on_shutdown)
    return app


async def on_shutdown(app: web.Application) -> None:
    """Close aiohttp client session on shutdown."""
    await app["session"].close()
