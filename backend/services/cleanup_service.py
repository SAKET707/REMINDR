from datetime import datetime, timedelta, timezone
from core.database import SessionLocal
from models.email import Email
from models.reminder import Reminder
# we need to clean reminder and email tables so they dont only fill but clears past mails also

import logging
logger = logging.getLogger(__name__)

class CleanupService:

    GRACE_PERIOD = timedelta(minutes=10) # safety buffer for failures or delayed processing.

    @staticmethod
    def cleanup():
        logger.info("Cleanup job started")

        db = SessionLocal()

        try:

            cutoff = (
                datetime.now(timezone.utc)
                - CleanupService.GRACE_PERIOD
            )

            emails = (
                db.query(Email)
                .join(Email.reminders)
                .filter(
                    Reminder.status == "SENT",
                    Reminder.sent_at <= cutoff,
                )
                .all()
            )

            if not emails:
                logger.info("No processed emails to clean")
                return

            logger.info(
                "Cleaning %d processed email(s)",
                len(emails),
            )

            for email in emails:
                db.delete(email) # cascade delete orphans is there

            db.commit()

            logger.info("Cleanup completed")

        except Exception:

            db.rollback()
            logger.exception("Cleanup job failed")
            raise

        finally:

            db.close()