from __future__ import annotations

from typing import Any, Dict

from .emoji import DiscordEmoji


class DiscordReaction:
    """https://discord.com/developers/docs/resources/message#get-channel-messages"""

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def emoji(self) -> DiscordEmoji:
        """str: 'emoji'"""
        return DiscordEmoji(self._data["emoji"])
