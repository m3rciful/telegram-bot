"""Tests for command management utilities."""

from __future__ import annotations

import asyncio

import pytest
from telegram import BotCommand

import utils.commands as commands


class DummyBot:
    """Minimal bot stub used for testing."""

    def __init__(self) -> None:
        self.received: list[BotCommand] | None = None

    async def set_my_commands(self, commands_list: list[BotCommand]) -> None:
        """Record the commands that would be set."""
        self.received = commands_list


class DummyApp:
    """Application stub exposing only the bot property."""

    def __init__(self) -> None:
        self.bot = DummyBot()


def test_command_registry_and_descriptions(monkeypatch):
    registry: list[commands.CommandMeta] = []
    monkeypatch.setattr(commands, "COMMAND_REGISTRY", registry, raising=False)

    @commands.command("Foo command")
    async def foo_command(update=None, context=None):
        pass

    @commands.command("Hidden", hidden=True)
    async def hidden_command(update=None, context=None):
        pass

    assert registry[0].name == "foo"
    assert registry[0].description == "Foo command"

    assert commands.get_commands_descriptions() == "/foo — Foo command"


def test_make_set_commands(monkeypatch):
    registry: list[commands.CommandMeta] = []
    monkeypatch.setattr(commands, "COMMAND_REGISTRY", registry, raising=False)

    @commands.command("Foo")
    async def foo_command(update=None, context=None):
        pass

    @commands.command("Bar", admin_only=True)
    async def bar_command(update=None, context=None):
        pass

    app = DummyApp()
    setter = commands.make_set_commands()
    asyncio.run(setter(app))

    assert app.bot.received == [BotCommand("foo", "Foo")]
