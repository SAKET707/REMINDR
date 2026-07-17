from datetime import datetime, timedelta, timezone

from core.database import SessionLocal
from models.email import Email
from models.reminder import Reminder
# we need to clean reminder and email tables so they dont only fill but clears past mails also

class CleanupService:

    GRACE_PERIOD = timedelta(minutes=10) # safety buffer for failures or delayed processing.

    @staticmethod
    def cleanup():
        print("🧹 Cleanup job started")

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
                print("No processed emails to clean.")
                return

            print(
                f"Cleaning {len(emails)} processed email(s)..."
            )

            for email in emails:
                db.delete(email) # cascade delete orphans is there

            db.commit()

            print("Cleanup completed.")

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()