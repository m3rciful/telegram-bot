"""Environment diagnostics utility.

Provides a single-responsibility function to log key environment details
such as Python version, OS platform, aiohttp, and python-telegram-bot versions.
Intended to be used at bot startup for diagnostic logging.
"""

import logging
import platform

import aiohttp
import telegram

startup_logger = logging.getLogger("startup")


def check_environment() -> None:
    """Log basic environment details such as Python, OS, and library versions."""
    startup_logger.info("🐍 Python version: %s", platform.python_version())
    startup_logger.info("🖥 Platform: %s %s", platform.system(), platform.release())
    startup_logger.info("🌐 aiohttp version: %s", aiohttp.__version__)
    startup_logger.info("🤖 python-telegram-bot version: %s", telegram.__version__)
