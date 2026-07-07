from datetime import datetime, timedelta, timezone

from core.database import SessionLocal
from models.email import Email
from models.reminder import Reminder


class CleanupService:

    GRACE_PERIOD = timedelta(minutes=10)

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
                db.delete(email)

            db.commit()

            print("Cleanup completed.")

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()