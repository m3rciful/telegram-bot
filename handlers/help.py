"""Handler for the /help command.

Dynamically generates a list of all available bot commands, excluding hidden ones,
and responds with a MarkdownV2-formatted message. Supports optional caching and
respects DEBUG mode to ensure fresh command list during development.
"""

import logging

from telegram import Update
from telegram.ext import ContextTypes
from utils.commands import get_commands_descriptions

# Exported command function for autoloading
__all__ = ["help_command"]

# Command description for Telegram's /menu
__descriptions__ = {"help_command": "Show available commands"}

logger = logging.getLogger("users")


async def help_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with a list of available commands in MarkdownV2 format."""
    logger.info("/help command used by %s", update.effective_user.id)

    text = "Use these commands to control me:\n\n"
    text += get_commands_descriptions()

    await update.message.reply_text(text, parse_mode="MarkdownV2")
