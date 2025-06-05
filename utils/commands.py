"""Command management utilities for the Telegram bot.

Provides helper functions to dynamically collect command descriptions from all
registered handlers, apply visibility filters (e.g. HIDDEN_COMMANDS), and set
the command list for the Telegram bot dynamically at runtime.
"""
import importlib
import pkgutil

import handlers
from config import HIDDEN_COMMANDS
from telegram import BotCommand
from telegram.ext import Application


def make_set_commands() -> callable:
    """Return an async command setter function with optional caching."""

    async def set_commands(application: Application) -> None:
        """Set commands on the bot instance, with filtering."""
        commands = []
        for _, module_name, _ in pkgutil.iter_modules(handlers.__path__):
            module = importlib.import_module(f"handlers.{module_name}")
            descriptions = getattr(module, "__descriptions__", {})
            for attr in getattr(module, "__all__", []):
                command = attr.replace("_command", "")
                if command in HIDDEN_COMMANDS:
                    continue
                description = descriptions.get(attr, command.capitalize())
                commands.append(BotCommand(command, description))
        await application.bot.set_my_commands(commands)

    return set_commands

def get_commands_descriptions() -> str:
    """Return a formatted string of all visible bot commands and their descriptions."""
    commands = []
    for _, module_name, _ in pkgutil.iter_modules(handlers.__path__):
        module = importlib.import_module(f"handlers.{module_name}")
        descriptions = getattr(module, "__descriptions__", {})
        for attr in getattr(module, "__all__", []):
            command = attr.replace("_command", "")
            if command in HIDDEN_COMMANDS:
                continue
            description = descriptions.get(attr, command.capitalize())
            commands.append((command, description))
    return "\n".join(f"/{cmd} — {desc}" for cmd, desc in commands)
