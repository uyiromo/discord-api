#!/usr/bin/env python3

import asyncio
import json
from asyncio import AbstractEventLoop
from email import message_from_string
from email.header import decode_header
from email.message import Message as EmailMessage
from logging import INFO, Formatter, Logger, StreamHandler, getLogger
from pathlib import Path
from typing import Dict, Optional

from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP, Envelope, Session

from api import DiscordAPI, fmt_text


def parse_smtp_content(content: str) -> tuple[str, Optional[str]]:
    """Parse SMTP mail content and extract message.

    Args:
        content (str): Raw SMTP mail content string

    Returns:
        tuple[str, Optional[str]]: Tuple of message body and subject
    """
    email_message: EmailMessage = message_from_string(content)
    body: str = ""

    def extract_text(payload: bytes | str | EmailMessage | None) -> str:
        """Extract text from email payload.

        Args:
            payload: Raw email payload

        Returns:
            str: Decoded text content
        """
        if isinstance(payload, bytes):
            return payload.decode()
        if isinstance(payload, str):
            return payload
        return ""

    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = extract_text(part.get_payload(decode=True))
                break
    else:
        body = extract_text(email_message.get_payload(decode=True))

    subject: Optional[str] = email_message.get("Subject")
    if subject and "=?utf-8?" in subject.lower():
        # Decode MIME encoded subject
        decoded_subject = decode_header(subject)[0][0]
        if isinstance(decoded_subject, bytes):
            subject = decoded_subject.decode()
        else:
            subject = str(decoded_subject)

    return body.strip(), subject


logger: Logger = getLogger("smtpd")
logger.setLevel(INFO)

handler: StreamHandler = StreamHandler()
handler.setFormatter(Formatter("[%(name)s] %(message)s"))
logger.addHandler(handler)


class CustomHandler:
    """Handler for processing incoming SMTP messages with authentication."""

    async def handle_DATA(self, server: SMTP, session: Session, envelope: Envelope) -> str:
        """Handle DATA command.

        Args:
            server: SMTP server instance.
            session: Current SMTP session.
            envelope: Current message envelope.

        Returns:
            str: Response code and message.
        """
        _ = server
        _ = session

        if envelope.content is None:
            logger.warning("No content in message")
            return "250 Empty message accepted"

        content: str
        if isinstance(envelope.content, str):
            content = envelope.content
        else:
            content = envelope.content.decode()

        # Parse the message
        body, subject = parse_smtp_content(content)

        logger.info(f"   FROM: {envelope.mail_from}")
        logger.info(f"     TO: {envelope.rcpt_tos}")
        logger.info(f"Subject: {subject}")
        logger.info(f" Length: {len(content)}")
        logger.info(" Content:")
        for line in body.splitlines():
            logger.info(f"> {line}")

        name: str
        domain: str
        name, domain = envelope.rcpt_tos[0].split("@", 1)
        if domain == "discord.localdomain":
            j: Path = Path(__file__).parent / "channels.json"
            tokens: Dict[str, str] = json.loads(j.read_text())[name]
            api: DiscordAPI = DiscordAPI(
                token=tokens["token"],
                chid=tokens["chid"],
            )
            api.CreateMessage(fmt_text(subject, body))  # type: ignore

        return "250 Message accepted for delivery"


async def main() -> None:
    controller: Controller = Controller(CustomHandler(), hostname="", port=25)
    controller.start()


if __name__ == "__main__":
    # basicConfig(level=INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    loop: AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()
        loop.close()
        logger.info("SMTP server stopped")
