"""Handler for the /help command.

Dynamically generates a list of all available bot commands, excluding hidden ones,
and responds with a MarkdownV2-formatted message. Supports optional caching and
respects DEBUG mode to ensure fresh command list during development.
"""

from telegram import Update
from telegram.ext import ContextTypes
from src.utils.commands import command, get_commands_descriptions


# Marks this function as a visible command with a description used in /help listing
@command("Show available commands")
async def help_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with a list of available commands."""
    text = "Use these commands to control me:\n\n"
    # Fetches all registered command descriptions, excluding hidden ones
    text += get_commands_descriptions()

    if update.message:
        await update.message.reply_text(text, parse_mode="MarkdownV2")
