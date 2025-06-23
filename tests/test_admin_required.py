"""Tests for the admin_required decorator."""

from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING

# Set minimal required environment so bot.config.Settings can initialize
os.environ.setdefault("BOT_TOKEN", "token")
os.environ.setdefault("WEBHOOK_URL", "https://example.com")

from bot.config import settings
from bot.utils.decorators import admin_required

if TYPE_CHECKING:
    import pytest


class DummyUser:
    """Minimal user stub with an id."""

    def __init__(self, user_id: int) -> None:
        """Initialize DummyUser with a user ID."""
        self.id = user_id


class DummyMessage:
    """Message stub recording reply_text calls."""

    def __init__(self) -> None:
        """Initialize DummyMessage with an empty replies list."""
        self.replies: list[str] = []

    async def reply_text(self, text: str) -> None:
        """Record the reply text."""
        self.replies.append(text)


class DummyUpdate:
    """Update stub exposing effective_user and message."""

    def __init__(self, user_id: int) -> None:
        """Initialize DummyUpdate with a user ID."""
        self.effective_user = DummyUser(user_id)
        self.message = DummyMessage()


class DummyContext:
    """Placeholder context object."""


def test_admin_allowed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure the wrapped function runs for the admin user."""
    monkeypatch.setattr(settings, "ADMIN_ID", 1, raising=False)

    called: bool = False

    @admin_required
    async def target(_update: DummyUpdate, _context: DummyContext) -> bool:
        nonlocal called
        called = True
        return True

    update = DummyUpdate(1)
    context = DummyContext()
    result = asyncio.run(target(update, context))

    if not called:
        msg = "Target function was not called for admin"
        raise AssertionError(msg)
    if result is not True:
        msg = "Return value from target not propagated"
        raise AssertionError(msg)
    if update.message.replies:
        msg = "reply_text should not be called for admin"
        raise AssertionError(msg)


def test_admin_denied(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure unauthorized users receive a message and the function is skipped."""
    monkeypatch.setattr(settings, "ADMIN_ID", 1, raising=False)

    called: bool = False

    @admin_required
    async def target(_update: DummyUpdate, _context: DummyContext) -> bool:
        nonlocal called
        called = True
        return True

    update = DummyUpdate(2)
    context = DummyContext()
    result = asyncio.run(target(update, context))

    if called:
        msg = "Target function should not be called for non-admin"
        raise AssertionError(msg)
    expected = ["You are not authorized to use this command."]
    if update.message.replies != expected:
        msg = f"Expected {expected}, got {update.message.replies}"
        raise AssertionError(msg)
    if result is not None:
        msg = "Wrapper should return None when unauthorized"
        raise AssertionError(msg)
