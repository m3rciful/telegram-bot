"""Configuration module for the Telegram bot.

Loads environment variables using `python-dotenv` and provides centralized access to
configuration values used throughout the project.

Sections:
- Telegram bot authentication
- Webhook settings for production deployment
- Logging configuration
- Admin access control

Refer to `.env.example` for variable definitions.
"""
import os

from dotenv import load_dotenv

# Load environment variables from the .env file into the system environment
load_dotenv()

# === Telegram Authentication ===
# Token used to authenticate the bot with Telegram API
BOT_TOKEN = os.getenv("BOT_TOKEN")

# === Webhook Settings ===
# Public HTTPS URL Telegram should use to send updates
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Webhook URL
WEBHOOK_LISTEN = os.getenv("WEBHOOK_LISTEN", "0.0.0.0")  # noqa: S104
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8443"))  # Webhook port

# === Logging ===
# Configuration for logging output level and file locations
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()  # Log level
LOG_DIR = os.getenv("LOG_DIR", "logs")  # Log folder
LOG_BOT_FILE = os.getenv("LOG_BOT_FILE", "bot.log")
LOG_ERRORS_FILE = os.getenv("LOG_ERRORS_FILE", "errors.log")

# === Admin ===
# Telegram user ID with admin access to the bot
ADMIN_ID = int(os.getenv("ADMIN_ID") or 0)  # Telegram user ID with admin access


# === Validation ===
# Ensures that required environment variables are defined before the bot starts
def validate_config() -> None:
    """Validate required environment variables are set."""
    missing: list[str] = []
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not WEBHOOK_URL:
        missing.append("WEBHOOK_URL")
    if missing:
        names = ", ".join(missing)
        msg = f"Missing required configuration variables: {names}"
        raise ValueError(msg)
