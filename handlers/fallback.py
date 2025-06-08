"""Fallback handler for unknown commands.

Logs unrecognized slash commands and provides a user-friendly response
prompting them to use /help. Ensures the bot gracefully handles invalid input.
"""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from utils.commands import command

logger = logging.getLogger("bot_bot")


# Registers this as a hidden command using the @command decorator.
# Hidden commands are not shown in the /help listing.
@command(hidden=True)

# Handles any unknown slash commands like /wrong, logs them, and replies with a hint.
async def unknown_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:  # noqa: ARG001
    """Handle unknown slash commands and guide user to /help."""
    if update.message and update.message.text.startswith("/"):
        logger.warning("Unknown command received: %s", update.message.text)
        await update.message.reply_text(
            "Unknown command. Type /help to see the available commands."
        )
