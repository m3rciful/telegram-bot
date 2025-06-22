"""Centralized logging setup for the Telegram bot.

Initializes a single logger with rotating file handlers,
error file output, and plain-text console output.
Supports structured formatting and configurable log levels.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from bot.config import settings


def get_logger() -> logging.Logger:
    """Return the main bot logger."""
    return logging.getLogger("bot")

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
    Path(settings.LOG_DIR).mkdir(parents=True, exist_ok=True)
    bot_log_path = Path(settings.LOG_DIR) / settings.LOG_BOT_FILE
    errors_log_path = Path(settings.LOG_DIR) / settings.LOG_ERRORS_FILE

    # Reduce verbosity of external libraries (e.g., HTTPX)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    rotating_bot_handler = RotatingFileHandler(
        bot_log_path, maxBytes=5_000_000, backupCount=3
    )
    rotating_bot_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    rotating_bot_handler.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

    error_handler = logging.FileHandler(errors_log_path)
    error_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    error_handler.setLevel(logging.ERROR)

    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

    configure_logger(
        "bot",
        [rotating_bot_handler, console_handler, error_handler],
        getattr(logging, settings.LOG_LEVEL, logging.DEBUG),
    )

