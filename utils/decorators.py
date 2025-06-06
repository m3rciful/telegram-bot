"""Utility decorators for bot handlers."""

from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

from config import ADMIN_ID
from telegram import Update
from telegram.ext import ContextTypes


def admin_required(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:  # noqa: E501
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
