"""Fallback handler for unknown commands.

Logs unrecognized slash commands and provides a user-friendly response
prompting them to use /help. Ensures the bot gracefully handles invalid input.
"""

import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger("bot_bot")

__all__ = ["unknown_command"]

# Hide this built-in command from menus
__hidden__: list[str] = ["unknown"]

# No admin-only commands here
__admin_only__: list[str] = []

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # noqa: ARG001
    """Handle unknown slash commands and guide user to /help."""
    if update.message and update.message.text.startswith("/"):
        logger.warning("Unknown command received: %s", update.message.text)
        await update.message.reply_text(
            "Unknown command. Type /help to see the available commands."
        )
