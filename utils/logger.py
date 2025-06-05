"""Centralized logging setup for the Telegram bot.

Initializes loggers with rotating file handlers, separate log files for components,
and colored console output using Colorama. Integrates multiple log levels and
structured formatting with support for user tagging in log messages.
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import ClassVar

from colorama import Fore, Style
from colorama import init as colorama_init
from config import (  # Import log level and log directory from centralized config
    LOG_DIR,
    LOG_LEVEL,
)

colorama_init()

# ColorFormatter for pretty colored logs in console
class ColorFormatter(logging.Formatter):
    """Custom logging formatter that adds color and user metadata to log messages."""

    COLORS: ClassVar[dict[int, str]] = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with colors and optional user metadata."""
        color = self.COLORS.get(record.levelno, "")
        reset = Style.RESET_ALL
        message = super().format(record)
        # Append user info to log if present in message
        if hasattr(record, "user_id") and hasattr(record, "user_name"):
            user_display = f"{record.user_name} (ID: {record.user_id})"
        elif hasattr(record, "user_id"):
            user_display = f"ID: {record.user_id}"
        elif hasattr(record, "user_name"):
            user_display = f"{record.user_name}"
        else:
            user_display = None

        if user_display:
            message += f" | 👤 {user_display}"
        return f"{color}{message}{reset}"

def configure_logger(name: str, handlers: list[logging.Handler], level: int) -> None:
    """Configure a logger with the given handlers and log level."""
    logger = logging.getLogger(name)
    if logger.level == logging.NOTSET:
        logger.setLevel(level)
    for handler in handlers:
        logger.addHandler(handler)

def setup_logging() -> None:
    """Set up logging with rotating files, color console output, and level filtering."""
    # Prepare logging directories and paths
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    bot_log_path = Path(LOG_DIR) / "bot.log"
    webhook_log_path = Path(LOG_DIR) / "webhook.log"
    errors_log_path = Path(LOG_DIR) / "errors.log"
    api_log_path = Path(LOG_DIR) / "api.log"
    users_log_path = Path(LOG_DIR) / "users.log"

    # Reduce verbosity of external libraries (e.g., HTTPX)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    rotating_bot_handler = RotatingFileHandler(
        bot_log_path, maxBytes=5_000_000, backupCount=3
    )
    rotating_bot_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    rotating_bot_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    webhook_handler = logging.FileHandler(webhook_log_path)
    webhook_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    webhook_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    error_handler = logging.FileHandler(errors_log_path)
    error_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    error_handler.setLevel(logging.ERROR)

    api_handler = logging.FileHandler(api_log_path)
    api_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    api_handler.setLevel(logging.INFO)

    users_handler = logging.FileHandler(users_log_path)
    users_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    users_handler.setLevel(logging.INFO)

    console_formatter = ColorFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    configure_logger(
        "bot_bot",
        [rotating_bot_handler, console_handler],
        getattr(logging, LOG_LEVEL, logging.DEBUG)
    )

    configure_logger(
        "startup",
        [console_handler, rotating_bot_handler],
        getattr(logging, LOG_LEVEL, logging.INFO)
    )

    configure_logger(
        "webhook",
        [webhook_handler, rotating_bot_handler, console_handler],
        getattr(logging, LOG_LEVEL, logging.INFO),
    )

    configure_logger(
        "errors",
        [error_handler, rotating_bot_handler],
        logging.ERROR,
    )

    configure_logger(
        "api",
        [api_handler, rotating_bot_handler],
        logging.INFO,
    )

    configure_logger("users", [users_handler, rotating_bot_handler], logging.INFO)

logger = logging.getLogger("bot_bot")
