from __future__ import annotations

from json import dumps
from typing import Any, Dict, List

from .reaction import DiscordReaction


class DiscordMessage:
    """https://discord.com/developers/docs/resources/message#get-channel-messages"""

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def id(self) -> str:
        """str: 'id'"""
        return self._data["id"]

    @property
    def channel_id(self) -> str:
        """str: 'channel_id'"""
        return self._data["channel_id"]

    @property
    def reactions(self) -> List[DiscordReaction]:
        """str: 'reactions'"""
        return [DiscordReaction(s) for s in self._data.get("reactions", [])]

    @property
    def content(self) -> str:
        """str: 'content'"""
        return self._data["content"]

    def __str__(self) -> str:
        return dumps(self._data, skipkeys=False, ensure_ascii=False, indent=4, sort_keys=True)
