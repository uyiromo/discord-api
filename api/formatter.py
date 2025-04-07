from __future__ import annotations

"""
Formatter module for Discord messages.

This module provides functions to format strings according to Discord markdown syntax.

Functions:
    fmt_bold(s): Formats a string as bold text.
    fmt_strike(s): Formats a string as strikethrough text.
    fmt_codeinline(s): Formats a string as inline code.
    fmt_codeblock(s): Formats a string as a code block.
    fmt_text(subject, message): Formats a subject and message into a standard format.
    fmt_exc(exc): Formats an exception with its traceback.
    furl_urls(s): Formats URLs in a string to make them non-embeddable in Discord.
"""


import re
from traceback import format_exc


def fmt_bold(s: str) -> str:
    return f"**{s}**"


def fmt_strike(s: str) -> str:
    return f"~~{s}~~"


def fmt_codeinline(s: str) -> str:
    return f"`{s}`"


def fmt_codeblock(s: str) -> str:
    return f"```\n{s}\n```"


def fmt_text(subject: str, message: str) -> str:
    return f"{fmt_bold(subject)}:\n{message}"


def fmt_exc(exc: Exception) -> str:
    return fmt_text(f"Exception: {str(exc)}", fmt_codeblock(format_exc()[:1900]))


def furl_urls(s: str) -> str:
    URL_REGEX: str = r"([a-z]+://[-a-zA-Z0-9@:%/._\+~#=]+)"
    return re.sub(URL_REGEX, r"<\1>", s)
