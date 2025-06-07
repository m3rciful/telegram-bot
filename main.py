"""Main entry point for starting the Telegram Bot.

This script sets up logging, checks environment variables,
and runs the bot using the run_telegram_bot function.
"""

import argparse
import logging
import sys

from config import RUN_MODE, validate_config
from core.runner import run_telegram_bot
from utils.environment import check_environment
from utils.logger import setup_logging


def main() -> None:
    """Set up environment and run the Telegram bot."""
    setup_logging()
    parser = argparse.ArgumentParser(description="Telegram Bot")
    parser.add_argument(
        "--mode",
        choices=["polling", "webhook"],
        default=RUN_MODE,
        help="Run mode: polling or webhook",
    )
    args = parser.parse_args()
    startup_logger = logging.getLogger("startup")
    try:
        validate_config()
    except ValueError:
        startup_logger.exception("Configuration error")
        sys.exit(1)
    check_environment()
    startup_logger.info("🚀 Starting Telegram Bot in %s mode", args.mode)
    run_telegram_bot(args.mode)


if __name__ == "__main__":
    main()
