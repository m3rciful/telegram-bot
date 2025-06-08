"""Administrative commands for the bot."""

from telegram import Update
from telegram.ext import ContextTypes

from utils.commands import command
from utils.decorators import admin_required


# Registers an admin-only command with description shown in /help
@command("Secret admin command", admin_only=True)
# Ensures only the admin (by ID) can run this command
@admin_required
async def secret_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond with a secret message for admins."""
    if update.message:
        await update.message.reply_text("🤫 This is a secret admin command.")
