import argparse
import logging
import sys

from pydantic import ValidationError

from src.config import settings
from src.core.runner import run_telegram_bot
from src.utils.environment import check_environment
from src.utils.logger import setup_logging


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the command line interface."""
    parser = argparse.ArgumentParser(description="Telegram Bot")
    parser.add_argument(
        "--mode",
        choices=["polling", "webhook"],
        default=settings.RUN_MODE,
        help="Run mode: polling or webhook",
    )
    parser.add_argument(
        "--diagnostics",
        action="store_true",
        help="Log environment diagnostics on startup",
    )
    return parser


def cli(argv: list[str] | None = None) -> None:
    """Entry point executed by ``main.py`` and tests."""
    setup_logging()
    parser = create_parser()
    args = parser.parse_args(argv)
    startup_logger = logging.getLogger("startup")
    try:
        _ = settings  # triggers validation by Pydantic BaseSettings
    except (ValueError, ValidationError):
        startup_logger.exception("Configuration validation error")
        sys.exit(1)
    if args.diagnostics:
        check_environment()
    startup_logger.info("🚀 Starting Telegram Bot in %s mode", args.mode)
    run_telegram_bot(args.mode)
