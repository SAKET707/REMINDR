import base64 # gmail sends in base64url encoded form so here decode is reqd
from datetime import datetime
from email.utils import parsedate_to_datetime # converts email date format correctly
# to convert raw gmail json to useful json/ clean py dict
from bs4 import BeautifulSoup # we will use to parse html and other to clean data


class ParserService:

    @staticmethod
    def _decode(data: str) -> str: # _ becos only parser service should use this, it is private
        """Decode Gmail base64url encoded text."""

        if not data:
            return ""

        decoded = base64.urlsafe_b64decode(data.encode("UTF-8")) # not standard base 64 but base 64 url

        return decoded.decode("utf-8", errors="ignore") # base 64 decoding returns bytes , need python string
                                    # ignore becos even if 1 invalid char occur dont crash but ignore/skiip bad bytes n continue

    @staticmethod
    def _clean_html(html: str) -> str: # llm dont need <h1> <p> tags so we remove them and clean the mail to plain txt
        """Convert HTML into readable plain text."""

        soup = BeautifulSoup(html, "html.parser")

        # remove scripts/styles
        for tag in soup(["script", "style"]): # these are noise not content -> script->js , styles->css
            tag.decompose()

        return soup.get_text(separator="\n", strip=True) # extract only text.

    @staticmethod
    def _extract_body(payload: dict) -> str: # it is recursive becos email can get into long depth, recursion handles any nesting
        """
        Recursively extracts the email body.
        """

        mime = payload.get("mimeType", "") # Multipurpose Internet Mail Extensions.it tels what kind of content

        # Plain text
        if mime == "text/plain":
            body = payload.get("body", {}).get("data")
            return ParserService._decode(body)

        # HTML
        if mime == "text/html":
            body = payload.get("body", {}).get("data")
            html = ParserService._decode(body)
            return ParserService._clean_html(html)

        # Multipart like html plain text attachments etc etc
        if "parts" in payload:

            for part in payload["parts"]:

                text = ParserService._extract_body(part)

                if text.strip():
                    return text

        return ""

    @staticmethod
    def parse(message: dict) -> dict:

        payload = message["payload"] # get gmail payload

        headers = {
            h["name"]: h["value"]
            for h in payload.get("headers", [])
        }
        # gmail gives a list of dict having key as name n value as value so we store them now to get later O(1) lookup

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