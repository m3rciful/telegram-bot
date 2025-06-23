import os

# Ensure required environment variables for bot.config are set before import
os.environ.setdefault("BOT_TOKEN", "dummy")
os.environ.setdefault("WEBHOOK_URL", "https://example.com")

from bot.utils.markdown import escape_markdown, mdv2_format


def test_escape_markdown_versions() -> None:
    """Escape characters for Markdown V1 and V2."""
    text_v1 = "_*`["
    expected_v1 = "\\_\\*\\`\\["
    result_v1 = escape_markdown(text_v1, version=1)
    if result_v1 != expected_v1:
        message = f"Expected '{expected_v1}', got '{result_v1}'"
        raise AssertionError(message)

    text_v2 = "_*[]()~`>#+-=|{}.!"
    expected_v2 = (
        "\\_\\*\\[\\]\\(\\)\\~\\`\\>\\#\\+\\-\\=\\|\\{\\}\\.\\!"
    )
    result_v2 = escape_markdown(text_v2, version=2)
    if result_v2 != expected_v2:
        message = f"Expected '{expected_v2}', got '{result_v2}'"
        raise AssertionError(message)


def test_escape_markdown_entity_types() -> None:
    """Verify that entity_type chooses the correct escape set."""
    text = "*`)"
    default = escape_markdown(text, version=2)
    if default != "\\*\\`\\)":
        message = f"Expected '\\*\\`\\)', got '{default}'"
        raise AssertionError(message)

    pre = escape_markdown(text, version=2, entity_type="pre")
    if pre != "*\\`)":
        message = f"Expected '*\\`)', got '{pre}'"
        raise AssertionError(message)

    text_link = escape_markdown(text, version=2, entity_type="text_link")
    if text_link != "*`\\)":
        message = f"Expected '*`\\)', got '{text_link}'"
        raise AssertionError(message)


def test_mdv2_format_only_escapes_values() -> None:
    """Variables are escaped inside the template, static text is untouched."""
    result = mdv2_format("*{name}* _unchanged_", name="John_Doe")
    if result != "*John\\_Doe* _unchanged_":
        message = f"Expected '*John\\_Doe* _unchanged_', got '{result}'"
        raise AssertionError(message)
