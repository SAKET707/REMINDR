import base64
from datetime import datetime
from email.utils import parsedate_to_datetime

from bs4 import BeautifulSoup


class ParserService:

    @staticmethod
    def _decode(data: str) -> str:
        """Decode Gmail base64url encoded text."""

        if not data:
            return ""

        decoded = base64.urlsafe_b64decode(data.encode("UTF-8"))

        return decoded.decode("utf-8", errors="ignore")

    @staticmethod
    def _clean_html(html: str) -> str:
        """Convert HTML into readable plain text."""

        soup = BeautifulSoup(html, "html.parser")

        # remove scripts/styles
        for tag in soup(["script", "style"]):
            tag.decompose()

        return soup.get_text(separator="\n", strip=True)

    @staticmethod
    def _extract_body(payload: dict) -> str:
        """
        Recursively extracts the email body.
        """

        mime = payload.get("mimeType", "")

        # Plain text
        if mime == "text/plain":
            body = payload.get("body", {}).get("data")
            return ParserService._decode(body)

        # HTML
        if mime == "text/html":
            body = payload.get("body", {}).get("data")
            html = ParserService._decode(body)
            return ParserService._clean_html(html)

        # Multipart
        if "parts" in payload:

            for part in payload["parts"]:

                text = ParserService._extract_body(part)

                if text.strip():
                    return text

        return ""

    @staticmethod
    def parse(message: dict) -> dict:

        payload = message["payload"]

        headers = {
            h["name"]: h["value"]
            for h in payload.get("headers", [])
        }

        received = headers.get("Date")

        received_at = None

        if received:
            received_at = parsedate_to_datetime(received)

        body = ParserService._extract_body(payload)

        return {
            "gmail_message_id": message["id"],
            "thread_id": message["threadId"],
            "history_id": message["historyId"],
            "sender": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "received_at": received_at,
            "body": body,
        }