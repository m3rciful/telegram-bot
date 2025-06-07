"""Dynamic handler loader for the Telegram bot.

Imports all modules inside the ``handlers`` package so their decorators run and
register the contained commands. Callback query handlers can still be declared
via a ``__callbacks__`` dictionary inside each module.
"""
import importlib
import pkgutil

import handlers
from telegram.ext import Application, CallbackQueryHandler, CommandHandler
from utils.commands import COMMAND_REGISTRY
from utils.logger import logger


def register_handlers(app: Application) -> None:
    """Auto-register handlers from the ``handlers`` package."""
    for _, module_name, _ in pkgutil.iter_modules(handlers.__path__):
        try:
            module = importlib.import_module(f"handlers.{module_name}")
        except Exception as exc:  # noqa: BLE001
            logger.exception(
                "Failed to import handler module %s: %s",
                module_name,
                exc,
            )
            continue

        # Register callback query handlers
        for attr, meta in getattr(module, "__callbacks__", {}).items():
            callback_func = getattr(module, attr)
            pattern = meta.get("pattern")
            app.add_handler(CallbackQueryHandler(callback_func, pattern=pattern))

    # Register all command handlers once after importing modules
    seen_commands: set[str] = set()
    for meta in COMMAND_REGISTRY:
        if meta.name in seen_commands:
            continue

        seen_commands.add(meta.name)
        app.add_handler(CommandHandler(meta.name, meta.func))
