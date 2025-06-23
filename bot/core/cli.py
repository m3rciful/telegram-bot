import argparse
import sys

from pydantic import ValidationError

from bot.config import settings
from bot.core.runner import run_telegram_bot
from bot.utils.logger import logger, setup_logging


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the command line interface."""
    parser = argparse.ArgumentParser(description="Telegram Bot")
    parser.add_argument(
        "--mode",
        choices=["polling", "webhook"],
        default=settings.RUN_MODE,
        help="Run mode: polling or webhook",
    )
    return parser


def cli(argv: list[str] | None = None) -> None:
    """Entry point executed by ``main.py`` and tests."""
    setup_logging()
    parser = create_parser()
    args = parser.parse_args(argv)
    try:
        settings.model_validate(settings.model_dump())
    except (ValueError, ValidationError):
        logger.exception("Configuration validation error")
        sys.exit(1)

    logger.info("🚀 Starting Telegram Bot in %s mode", args.mode)
    run_telegram_bot(args.mode)
