"""Example handler to demonstrate alias usage.

Shows how a command can be registered with an alias,
and responds with confirmation of invocation.
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from src.utils.commands import command


# Marks this function as a visible command with a description used in /help listing
@command("Demonstrate alias support", aliases=["a"])
async def alias_command(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Reply confirming that the alias command (or its alias) was triggered."""
    text = escape_markdown(
        "You triggered the /alias command (or its alias /a).", version=2
    )

    if update.message:
        await update.message.reply_text(text, parse_mode="MarkdownV2")
