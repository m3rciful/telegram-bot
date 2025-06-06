"""Markdown escaping utility for Telegram bots.

Provides a version-aware function to escape special Markdown characters
required by Telegram's MarkdownV1 and MarkdownV2 formats. Supports
entity-type specific escaping for safer formatting in messages.
"""
import logging
import re

TELEGRAM_MD_V1 = 1
TELEGRAM_MD_V2 = 2

logger = logging.getLogger("bot_bot")

def escape_markdown(text: str, version: int = 2, entity_type: str | None = None) -> str:
    """Escape Telegram Markdown special characters for MarkdownV1 or MarkdownV2.

    Args:
        text (str): The text to escape.
        version (int): Telegram Markdown version (1 or 2). Defaults to 2.
        entity_type (Optional[str]): Entity type for selective escaping in MarkdownV2.
            Options: "pre", "code", "text_link".

    """
    if int(version) == TELEGRAM_MD_V1:
        escape_chars = r"_*`["
    elif int(version) == TELEGRAM_MD_V2:
        if entity_type in {"pre", "code"}:
            escape_chars = r"\`"
        elif entity_type == "text_link":
            escape_chars = r"\)"
        else:
            escape_chars = r"_*\[\]()~`>#+\-=|{}.!"
    else:
        error_msg = "Markdown version must be either 1 or 2!"
        raise ValueError(error_msg)

    escaped = re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)
    logger.debug("Escaped MarkdownV%s: %s", version, escaped)
    if version == TELEGRAM_MD_V2 and re.search(r"(\*{2,}|_{2,})", text):
        logger.warning("Possible nested or excessive bold/italic syntax detected.")
    logger.debug(
        "Escaping text for Markdown v%s with entity='%s'",
        version,
        entity_type,
    )
    return escaped
