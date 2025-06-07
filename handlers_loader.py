"""Dynamic handler loader for the Telegram bot.

Iterates through all modules in the handlers package and automatically registers:
- command handlers listed in `__all__`
- callback query handlers listed in `__callbacks__`

This enables modular structure without manual handler imports.
"""
import importlib
import pkgutil

import handlers
from telegram.ext import Application, CallbackQueryHandler, CommandHandler
from utils.logger import logger


def register_handlers(app: Application) -> None:
    """Auto-registers handlers from all modules."""
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

        # Register command handlers
        for attr in getattr(module, "__all__", []):
            handler_func = getattr(module, attr)
            command = attr.replace("_command", "")
            app.add_handler(CommandHandler(command, handler_func))

        # Register callback query handlers
        for attr, meta in getattr(module, "__callbacks__", {}).items():
            callback_func = getattr(module, attr)
            pattern = meta.get("pattern")
            app.add_handler(CallbackQueryHandler(callback_func, pattern=pattern))
