#!/usr/bin/env python3

import json
from enum import Enum, auto
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import requests

from .message import DiscordMessage


class RequestType(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()


class DiscordAPI:
    """Discord API (OAuth2)

    Scopes (Permission: 75840)
        bot (Send Messages, Manage Messages, Read Message History, Add Reactions)

    """

    def __init__(
        self,
        token: str,
        chid: str,
    ):
        self._token: str = token
        self._chid: str = chid

    def _call(
        self,
        type: RequestType,
        url: str,
        headers: Dict[str, Any],
        params: Dict[str, Any],
        data: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        headers["Authorization"] = f"Bot {self._token}"
        headers["User-Agent"] = "DiscordBot"

        method = requests.get  # default
        match type:
            case RequestType.GET:
                method = requests.get  # type: ignore[assignment]
            case RequestType.POST:
                method = requests.post  # type: ignore[assignment]
            case RequestType.PUT:
                method = requests.put  # type: ignore[assignment]
            case RequestType.DELETE:
                method = requests.delete  # type: ignore[assignment]
            case _:
                raise ValueError(f"{type} is now supported")

        if data:
            return method(url, headers=headers, params=params, data=json.dumps(data))
        else:
            return method(url, headers=headers, params=params)

    def CreateReaction(self, msg: DiscordMessage, emoji: str) -> None:
        """
        PUT /channels/{channel.id}/messages/{message.id}/reactions/{emoji}/@me

        https://discord.com/developers/docs/resources/message#create-reaction
        """
        _: requests.Response = self._call(
            RequestType.PUT,
            f"https://discord.com/api/channels/{msg.channel_id}/messages/{msg.id}/reactions/{quote(emoji)}/@me",
            headers={},
            params={},
            data={},
        )

        return

    def GetChannelMessages(self) -> List[DiscordMessage]:
        """
        GET /channels/{channel.id}/messages

        https://discord.com/developers/docs/resources/message#get-channel-messages
        """
        r: requests.Response = self._call(
            RequestType.GET,
            f"https://discord.com/api/channels/{self._chid}/messages",
            headers={},
            params={"limit": 100},
            data={},
        )

        return [DiscordMessage(m) for m in r.json()]

    def DeleteMessage(
        self,
        msg: DiscordMessage,
    ) -> None:
        """
        DELETE /channels/{channel.id}/messages/{message.id}

        https://discord.com/developers/docs/resources/message#delete-message
        """
        _: requests.Response = self._call(
            RequestType.DELETE,
            f"https://discord.com/api/channels/{msg.channel_id}/messages/{msg.id}",
            headers={},
            params={},
            data={},
        )

        return

    def CreateMessage(
        self,
        content: str,
    ) -> None:
        """
        POST /channels/{channel.id}/messages

        https://discord.com/developers/docs/resources/message#create-message
        """
        _: requests.Response = self._call(
            RequestType.POST,
            f"https://discord.com/api/channels/{self._chid}/messages",
            headers={"Content-Type": "application/json"},
            params={},
            data={"content": content},
        )

        return
