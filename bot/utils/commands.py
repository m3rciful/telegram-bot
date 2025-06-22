"""Command management utilities for the Telegram bot.

Provides helper functions and helpers for registering command handlers and
generating their descriptions for the bot's command list.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from telegram import BotCommand

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from telegram.ext import Application


@dataclass(slots=True)
class CommandMeta:
    """Metadata about a registered command."""

    name: str
    func: Callable[..., Awaitable[None]]
    description: str
    hidden: bool = False
    admin_only: bool = False
    aliases: list[str] = field(default_factory=list)


COMMAND_REGISTRY: list[CommandMeta] = []


def command(
    description: str | None = None,
    *,
    hidden: bool = False,
    admin_only: bool = False,
    aliases: list[str] | None = None,
) -> Callable[[Callable[..., Awaitable[None]]], Callable[..., Awaitable[None]]]:
    """Register a command handler with optional metadata."""

    def decorator(
        func: Callable[..., Awaitable[None]],
    ) -> Callable[..., Awaitable[None]]:
        command_name = func.__name__.replace("_command", "")
        COMMAND_REGISTRY.append(
            CommandMeta(
                name=command_name,
                func=func,
                description=description or command_name.capitalize(),
                hidden=hidden,
                admin_only=admin_only,
                aliases=aliases or [],
            )
        )
        return func

    return decorator


def make_set_commands() -> Callable[[Application], Awaitable[None]]:
    """Return an async command setter function with optional caching."""

    async def set_commands(application: Application) -> None:
        """Set commands on the bot instance, with filtering."""
        commands = [
            BotCommand(meta.name, meta.description)
            for meta in COMMAND_REGISTRY
            if not meta.hidden and not meta.admin_only
        ]
        await application.bot.set_my_commands(commands)

    return set_commands


def get_commands_descriptions() -> str:
    """Return a formatted string of all visible bot commands and their descriptions."""
    visible_commands = [
        (meta.name, meta.description)
        for meta in COMMAND_REGISTRY
        if not meta.hidden and not meta.admin_only
    ]
    return "\n".join(f"/{cmd} — {desc}" for cmd, desc in visible_commands)
