from collections import defaultdict
from datetime import datetime, timezone
from core.database import SessionLocal # this creates its own session 
from services.reminder_service import ReminderService # we use this to get due reminders
from services.tele_noti_service import TeleNotiService # formats the msg and sends it

import logging
logger = logging.getLogger(__name__)

class NotificationService:

    @staticmethod
    def process_due_reminders(): # apscheduler calls this periodically

        db = SessionLocal() # this creates its own session/fresh transaction becos, this service is not called by fastapi endpoint but rather scheduler

        try:

            reminders = ReminderService.get_due_reminders(db) # get due reminders
            logger.info("Notification scheduler started")
            logger.info(
                "Found %d due reminder(s)",
                len(reminders),
            )

            if not reminders:
                return

            reminders_by_user = defaultdict(list)

            for reminder in reminders: # it groups reminders based on userId 

                user = reminder.email.user

                reminders_by_user[user.id].append(reminder)

            for reminder_list in reminders_by_user.values():

                user = reminder_list[0].email.user
                logger.info(
                    "Sending %d reminder(s) to %s",
                    len(reminder_list),
                    user.email,
                )

                if not user.telegram_chat_id: # if telegram not connected then skip no crash
                    logger.info(
                        "Skipping reminders for %s because Telegram is not connected",
                        user.email,
                    )
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

                logger.info(
                    "Telegram notification sent to %s",
                    user.email,
                )

            db.commit()

        except Exception:

            db.rollback()
            logger.exception(
                "Notification scheduler failed"
            )
            raise

        finally:

            db.close()


# defaultdict -> becos in normal dict suppose 1. d={} 2. d[5].append(...) then it keyErrors n crashes
#  with this py creates { 5:[] } then append works.