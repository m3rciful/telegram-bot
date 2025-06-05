"""Configuration module for the Telegram bot.

Loads environment variables using `python-dotenv` and exposes strongly-typed
constants for use throughout the project. Includes configuration for:
- Telegram API keys and bot token
- Logging level and directory
- Webhook mode and URL
- Admin ID
- Hidden commands list
"""
import os

from dotenv import load_dotenv

# Load environment variables from the .env file into the system environment
load_dotenv()

# === Telegram ===
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Telegram Bot API token

# === Logging ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()  # Log level
LOG_DIR = os.getenv("LOG_DIR", "logs")  # Log folder

# === Webhook ===
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Webhook URL
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")  # Webhook path endpoint
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8443"))  # Webhook port

# === Admin ===
ADMIN_ID = int(os.getenv("ADMIN_ID") or 0)  # Telegram user ID with admin access

#== Hidden Commands ===
HIDDEN_COMMANDS = os.getenv("HIDDEN_COMMANDS", "")
HIDDEN_COMMANDS = [cmd.strip() for cmd in HIDDEN_COMMANDS.split(",") if cmd.strip()]
