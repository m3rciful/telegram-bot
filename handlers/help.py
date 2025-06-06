"""Handler for the /help command.

Dynamically generates a list of all available bot commands, excluding hidden ones,
and responds with a MarkdownV2-formatted message. Supports optional caching and
respects DEBUG mode to ensure fresh command list during development.
"""

from telegram import Update
from telegram.ext import ContextTypes
from utils.commands import get_commands_descriptions

# Exported command function for autoloading
__all__ = ["help_command"]

# Command description for Telegram's /menu
__descriptions__ = {"help_command": "Show available commands"}

# Commands hidden from /help or menu
__hidden__: list[str] = []

# Admin only commands
__admin_only__: list[str] = []


async def help_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with a list of available commands."""
    text = "Use these commands to control me:\n\n"
    text += get_commands_descriptions()

    if update.message:
        await update.message.reply_text(text, parse_mode="MarkdownV2")
