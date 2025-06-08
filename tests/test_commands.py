"""Tests for command management utilities."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from src.utils import commands
from telegram import BotCommand

if TYPE_CHECKING:
    import pytest


class DummyBot:
    """Minimal bot stub used for testing."""

    def __init__(self) -> None:
        """Initialize the DummyBot with no received commands."""
        self.received: list[BotCommand] | None = None

    async def set_my_commands(self, commands_list: list[BotCommand]) -> None:
        """Record the commands that would be set."""
        self.received = commands_list


class DummyApp:
    """Application stub exposing only the bot property."""

    def __init__(self) -> None:
        """Initialize the DummyApp with a DummyBot instance."""
        self.bot = DummyBot()


def test_command_registry_and_descriptions(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the command registry and command descriptions functionality."""
    registry: list[commands.CommandMeta] = []
    monkeypatch.setattr(commands, "COMMAND_REGISTRY", registry, raising=False)

    @commands.command("Foo command")
    async def foo_command(update: object = None, context: object = None) -> None:
        pass

    @commands.command("Hidden", hidden=True)
    async def hidden_command(update: object = None, context: object = None) -> None:
        pass

    if registry[0].name != "foo":
        msg = f"Expected registry[0].name to be 'foo', got {registry[0].name}"
        raise AssertionError(msg)
    if registry[0].description != "Foo command":
        msg = (
            "Expected registry[0].description to be 'Foo command', got "
            f"{registry[0].description}"
        )
        raise AssertionError(msg)

    if commands.get_commands_descriptions() != "/foo — Foo command":
        msg = (
            "Expected '/foo — Foo command', got "
            f"'{commands.get_commands_descriptions()}'"
        )
        raise AssertionError(
            msg
        )


def test_make_set_commands(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the make_set_commands utility for setting bot commands."""
    registry: list[commands.CommandMeta] = []
    monkeypatch.setattr(commands, "COMMAND_REGISTRY", registry, raising=False)

    @commands.command("Foo")
    async def foo_command(update: object = None, context: object = None) -> None:
        pass

    @commands.command("Bar", admin_only=True)
    async def bar_command(update: object = None, context: object = None) -> None:
        pass

    app = DummyApp()
    setter = commands.make_set_commands()
    asyncio.run(setter(app))

    if app.bot.received != [BotCommand("foo", "Foo")]:
        msg = f"Expected {[BotCommand('foo', 'Foo')]}, got {app.bot.received}"
        raise AssertionError(msg)
