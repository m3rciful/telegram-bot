"""Main entry point for starting the Telegram Bot.

This script sets up logging, checks environment variables,
and runs the bot using the run_telegram_bot function.
"""

import logging

from core.runner import run_telegram_bot
from utils.environment import check_environment
from utils.logger import setup_logging


def main() -> None:
    """Set up environment and run the Telegram bot."""
    setup_logging()
    check_environment()
    startup_logger = logging.getLogger("startup")
    startup_logger.info("🚀 Starting Telegram Bot")
    run_telegram_bot()


if __name__ == "__main__":
    main()
