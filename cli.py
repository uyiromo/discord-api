#!/usr/bin/env python3
from __future__ import annotations

from argparse import ArgumentParser, Namespace
from json import loads
from logging import INFO, Formatter, StreamHandler, getLogger
from pathlib import Path
from typing import Dict

from api import DiscordAPI

logger = getLogger("discord-cli")

handler = StreamHandler()
handler.setFormatter(Formatter("[%(name)s] %(message)s"))
logger.addHandler(handler)
logger.setLevel(INFO)


if __name__ == "__main__":
    # args
    parser = ArgumentParser(description="Discord API CLI")
    parser.add_argument("--channels-json", type=Path, required=True)
    parser.add_argument("--channel", type=str, required=True)
    parser.add_argument("message", nargs=1, type=str)

    args: Namespace = parser.parse_args()
    logger.info("args:")
    logger.info(f"  channels-json: {args.channels_json}")
    logger.info(f"        channel: {args.channel}")
    logger.info(f"        message: {args.message}")

    chj: Dict[str, Dict[str, str]] = loads(args.channels_json.read_text())
    token: str = chj[args.channel]["token"]
    chid: str = chj[args.channel]["chid"]

    logger.info("API data:")
    logger.info(f"  token: {token}")
    logger.info(f"   chid: {chid}")

    DiscordAPI(
        token=token,
        chid=chid,
    ).CreateMessage(args.message[0])
