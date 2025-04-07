#!/usr/bin/env python3
from __future__ import annotations

from argparse import ArgumentParser, Namespace
from logging import INFO, Formatter, StreamHandler, getLogger

from api import DiscordAPI

logger = getLogger("discord-cli")

handler = StreamHandler()
handler.setFormatter(Formatter("[%(name)s] %(message)s"))
logger.addHandler(handler)
logger.setLevel(INFO)


if __name__ == "__main__":
    # args
    parser = ArgumentParser(description="Discord API CLI")
    parser.add_argument("--chid", type=str, required=True, help="Channel ID")
    parser.add_argument("--token", type=str, required=True, help="Token")
    parser.add_argument("message", nargs=1, type=str)

    args: Namespace = parser.parse_args()
    logger.info("args:")
    logger.info(f"   chid: {args.chid}")
    logger.info(f"  token: {args.token}")
    logger.info(f"message: {args.message}")

    DiscordAPI(
        token=args.token,
        chid=args.chid,
    ).CreateMessage(args.message[0])
