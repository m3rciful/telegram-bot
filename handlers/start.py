"""Handler for the /start command in the MTR Bot.

Sends a greeting message and basic usage instructions to the user.
"""

# Exported function name for autoload registration
__all__ = ["start_command"]

# Description used in Telegram's /menu
__descriptions__ = {"start_command": "Launch the bot"}

import logging

from telegram import Update
from telegram.ext import ContextTypes
from utils.markdown import escape_markdown

logger = logging.getLogger("bot_bot")


# Command handler for /start - greets the user
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send greeting message to user on /start command."""
    logger.debug("📥 Received command: %s", update.message.text)
    _ = context
    # /start command: greet the user
    text = escape_markdown(
        "Welcome! This is a base template for a Telegram bot.\n"
        "Use this bot as a starting point to build your own functionality.\n\n"
        "You can see the list of commands by typing /help.",
        version=2
    )
    await update.message.reply_text(text, parse_mode="MarkdownV2")

