"""
Application configuration using environment variables.

Structured using Pydantic BaseSettings for validation and override support.
"""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Uses Pydantic BaseSettings for validation and override support.
    """

    # === Telegram Authentication ===
    BOT_TOKEN: str
    ADMIN_ID: int = 0

    # === Run Mode ===
    RUN_MODE: str = "webhook"

    # === Webhook Settings ===
    WEBHOOK_URL: str
    WEBHOOK_LISTEN: str = "0.0.0.0"  # noqa: S104
    WEBHOOK_PORT: int = 8443

    # === Logging ===
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_BOT_FILE: str = "bot.log"
    LOG_ERRORS_FILE: str = "errors.log"

    # === File Paths ===
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    class Config:
        """Pydantic configuration for environment file settings."""

        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
