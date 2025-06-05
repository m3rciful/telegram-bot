"""Entry point for the Apex Legends Telegram bot.

Initializes logging, checks environment, and starts
the bot using polling or webhook based on configuration.
"""

import logging

from core.runner import run_bot
from utils.environment import check_environment
from utils.logger import setup_logging

startup_logger = logging.getLogger("startup")
startup_logger.info("🚀 Starting mtr bot")

if __name__ == "__main__":
    setup_logging()
    check_environment()
    run_bot()
