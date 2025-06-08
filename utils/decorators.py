"""
This module provides utility decorators for use with Telegram bot handlers.

- `admin_required`: A decorator to restrict command access to the configured admin user.
  It checks if the command issuer's Telegram ID matches the `ADMIN_ID` from the config.
  If not, it sends an unauthorized access message.
"""

from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

from config import ADMIN_ID
from telegram import Update
from telegram.ext import ContextTypes


def admin_required(
    func: Callable[..., Awaitable[Any]],
) -> Callable[..., Awaitable[Any]]:
    """Allow execution only for the configured ADMIN_ID."""

    @wraps(func)
    async def wrapper(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        *args: object,
        **kwargs: dict[str, object]
    ) -> None | bool:
        if update.effective_user and update.effective_user.id == ADMIN_ID:
            return await func(update, context, *args, **kwargs)
        if update.message:
            await update.message.reply_text(
                "You are not authorized to use this command."
            )
        return None

    return wrapper
