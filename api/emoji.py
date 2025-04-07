from __future__ import annotations

from typing import Any, Dict


class DiscordEmoji:
    STAR: str = "⭐"
    EYES: str = "👀"
    MUTE: str = "🔇"
    CHECK: str = "✅"

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def name(self) -> str:
        """str: 'name'"""
        return self._data["name"]
