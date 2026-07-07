from collections import defaultdict
from datetime import datetime, timezone

from core.database import SessionLocal
from services.reminder_service import ReminderService
from services.tele_noti_service import TeleNotiService


class NotificationService:

    @staticmethod
    def process_due_reminders():

        db = SessionLocal()

        try:

            reminders = ReminderService.get_due_reminders(db)
            print("Scheduler running...")
            print(f"Found {len(reminders)} due reminders")

            if not reminders:
                return

            reminders_by_user = defaultdict(list)

            for reminder in reminders:

                user = reminder.email.user

                reminders_by_user[user.id].append(reminder)

            for reminder_list in reminders_by_user.values():

                user = reminder_list[0].email.user
                print(f"Sending {len(reminder_list)} reminders to {user.email}")

                if not user.telegram_chat_id:
                    continue

                message = TeleNotiService.format_reminders(
                    reminder_list
                )

                TeleNotiService.send_message(
                    chat_id=user.telegram_chat_id,
                    text=message,
                )

                for reminder in reminder_list:

                    reminder.status = "SENT"
                    reminder.sent_at = datetime.now(
                        timezone.utc
                    )

                print("Telegram message sent")

            db.commit()

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()