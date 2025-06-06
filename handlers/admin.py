"""Administrative commands for the bot."""

from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_required

# Exported function name for autoload registration
__all__ = ["secret_command"]

# Description used in Telegram's /menu
__descriptions__ = {"secret_command": "Secret admin command"}

# No commands hidden specifically in this module
__hidden__: list[str] = []

# List of commands available only to admin
__admin_only__: list[str] = ["secret"]


@admin_required
async def secret_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond with a secret message for admins."""
    if update.message:
        await update.message.reply_text("🤫 This is a secret admin command.")
