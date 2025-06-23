"""Tests for the CLI entry point."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest


def _reload_cli() -> object:
    """Reload config and cli modules to apply environment changes."""
    from bot import config
    from bot.core import cli

    importlib.reload(config)
    return importlib.reload(cli)


def test_cli_polling(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure cli() passes provided mode argument to run_telegram_bot."""
    monkeypatch.setenv("BOT_TOKEN", "x")
    monkeypatch.setenv("WEBHOOK_URL", "https://example.com")
    monkeypatch.setenv("RUN_MODE", "webhook")

    cli = _reload_cli()

    received: list[str] = []

    def fake(mode: str) -> None:
        received.append(mode)

    monkeypatch.setattr(cli, "run_telegram_bot", fake)

    cli.cli(["--mode", "polling"])

    if received != ["polling"]:
        msg = f"Expected ['polling'], got {received}"
        raise AssertionError(msg)


def test_cli_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure cli() uses settings.RUN_MODE when no mode is provided."""
    monkeypatch.setenv("BOT_TOKEN", "x")
    monkeypatch.setenv("WEBHOOK_URL", "https://example.com")
    monkeypatch.setenv("RUN_MODE", "webhook")

    cli = _reload_cli()

    received: list[str] = []

    def fake(mode: str) -> None:
        received.append(mode)

    monkeypatch.setattr(cli, "run_telegram_bot", fake)

    cli.cli([])

    expected = cli.settings.RUN_MODE
    if received != [expected]:
        msg = f"Expected [{expected!r}], got {received}"
        raise AssertionError(msg)
