import collections.abc
import pkgutil
import sys
import types

import pytest
from bot.utils import commands


class DummyApp:
    """Minimal app with a handler list for testing."""

    def __init__(self) -> None:
        """Initialize DummyApp with an empty handlers list."""
        self.handlers = []

    def add_handler(self, handler: object) -> None:
        """Append a handler to the handlers list."""
        self.handlers.append(handler)


def test_register_handlers(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that handlers are registered correctly from mocked modules."""
    monkeypatch.setenv("BOT_TOKEN", "x")
    monkeypatch.setenv("WEBHOOK_URL", "https://example.com")
    from bot import handlers_loader
    registry: list[commands.CommandMeta] = []
    monkeypatch.setattr(commands, "COMMAND_REGISTRY", registry, raising=False)
    monkeypatch.setattr(handlers_loader, "COMMAND_REGISTRY", registry, raising=False)

    fake_pkg = types.ModuleType("bot.handlers")
    fake_pkg.__path__ = ["dummy"]

    mod_a = types.ModuleType("bot.handlers.first")
    mod_b = types.ModuleType("bot.handlers.second")

    @commands.command("First", aliases=["f"])
    async def foo_command(update: object = None, context: object = None) -> None:
        pass

    mod_a.foo_command = foo_command

    @commands.command("Second", aliases=["f"])
    async def bar_command(update: object = None, context: object = None) -> None:
        pass

    mod_b.bar_command = bar_command

    monkeypatch.setitem(sys.modules, "bot.handlers", fake_pkg)
    monkeypatch.setitem(sys.modules, "bot.handlers.first", mod_a)
    monkeypatch.setitem(sys.modules, "bot.handlers.second", mod_b)

    monkeypatch.setattr(handlers_loader, "handlers", fake_pkg, raising=False)

    def fake_iter_modules(
        path: list[str],
    ) -> collections.abc.Iterator[pkgutil.ModuleInfo]:
        if path != fake_pkg.__path__:
            msg = "Path does not match fake_pkg.__path__"
            raise AssertionError(msg)
        yield pkgutil.ModuleInfo(module_finder=None, name="first", ispkg=False)
        yield pkgutil.ModuleInfo(module_finder=None, name="second", ispkg=False)

    monkeypatch.setattr(pkgutil, "iter_modules", fake_iter_modules)

    app = DummyApp()
    handlers_loader.register_handlers(app)

    names = [next(iter(handler.commands)) for handler in app.handlers]
    msg = "Expected one 'foo' command handler"
    if names.count("foo") != 1:
        raise AssertionError(msg)
    msg = "Expected one 'bar' command handler"
    if names.count("bar") != 1:
        raise AssertionError(msg)
    msg = (
        "Expected one 'f' command handler"
    )
    if names.count("f") != 1:
        raise AssertionError(msg)
