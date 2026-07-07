from collections import defaultdict
import requests
from core.config import settings

class TeleNotiService:

    BASE_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"

    @staticmethod
    def send_message(chat_id: str, text: str):

        response = requests.post(
            f"{TeleNotiService.BASE_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown",
            },
            timeout=15,
        )

        response.raise_for_status()

    @staticmethod
    def format_reminders(reminders):

        lines = []

        lines.append("🔔 *REMINDR*")
        lines.append("")
        lines.append(
            f"You have *{len(reminders)}* reminder(s)."
        )
        lines.append("")

        for i, reminder in enumerate(reminders, start=1):

            email = reminder.email

            lines.append(
                f"*{i}. {email.subject}*"
            )

            lines.append(
                email.summary
            )

            if email.deadline:
                lines.append(
                    f"📅 Deadline: {email.deadline.strftime('%d %b %Y %H:%M UTC')}"
                )

            lines.append("")

        return "\n".join(lines)