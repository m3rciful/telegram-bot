"""Global error handler for the Telegram bot.

Captures and logs all exceptions raised during update processing,
and optionally notifies the user with a fallback message.
"""
import logging

from telegram import Update
from telegram.ext import ContextTypes


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors raised during update processing and optionally notify the user."""
    logging.getLogger("errors").error(
        "Exception while handling an update:",
        exc_info=context.error
    )
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text("⚠️ An unexpected error occurred.")
