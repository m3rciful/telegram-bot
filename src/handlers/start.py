"""Handler for the /start command in the MTR Bot.

Sends a greeting message and basic usage instructions to the user.
"""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from src.utils.commands import command
from src.utils.markdown import escape_markdown

logger = logging.getLogger("bot_bot")


# Register the /start command with a description shown in /help
@command("Launch the bot")
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send greeting message to user on /start command."""
    # Log the received command for debugging
    logger.debug("📥 Received command: %s", update.message.text)
    _ = context
    # Get user ID and greet the user with instructions
    user_id = update.effective_user.id if update.effective_user else "unknown"
    # /start command: greet the user
    text = escape_markdown(
        f"Hello! User ID: {user_id}\n\n"
        "This is a base template for a Telegram bot.\n"
        "Use this bot as a starting point to build your own functionality.\n\n"
        "You can see the list of commands by typing /help.",
        version=2,
    )
    await update.message.reply_text(text, parse_mode="MarkdownV2")
