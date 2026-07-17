from collections import defaultdict
import requests # communicate using http req
from core.config import settings
# this service knows how to send msg to telegram
class TeleNotiService:

    BASE_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}" # initialize once & reuse it 

    @staticmethod
    def send_message(chat_id: str, text: str):

        response = requests.post( # we send data so post
            f"{TeleNotiService.BASE_URL}/sendMessage", # POST / sendMessage but many more exists for photo , docs etc
            json={ # telegram bot expects json req body
                "chat_id": chat_id, # telegram gives every chat a unique id which doesnt change
                "text": text,
                "parse_mode": "Markdown", # w/ this telegram renders correctly like bold text etc. & more readablity
            },
            timeout=15, # after 15 seconds , raise an exception becos sometime telegram server hangs, so backend dont need to wait forever
                        # and no blockage of resources
        )

        response.raise_for_status()# telegram may return 500 , 404 , w/o this backend thinks everything succeeded. 
                                    #instead raise exception and rollback .

    @staticmethod
    def format_reminders(reminders):

        lines = []

        lines.append("🔔 *REMINDR*")
        lines.append("")
        lines.append(
            f"You have *{len(reminders)}* reminder(s)."
        )
        lines.append("")

        for i, reminder in enumerate(reminders, start=1): # start numbering like in points from 1. /// 2. ///

            email = reminder.email

            lines.append(
                f"*{i}. {email.subject}*"
            )

            lines.append(
                email.summary
            )

            if email.deadline:
                lines.append(
                    f"📅 Deadline: {email.deadline.strftime('%d %b %Y %H:%M UTC')}" # users prefers 18 Jul 2026 09:00 UTC format. 
                )

            lines.append("")

        return "\n".join(lines)