from datetime import datetime, timedelta, timezone

from core.database import SessionLocal
from models.user import User
from services.gmail_service import enable_gmail_watch


class GmailWatchService:

    RENEW_BEFORE = timedelta(days=1)

    @staticmethod
    def renew_expiring_watches():

        db = SessionLocal()

        try:

            now = datetime.now(timezone.utc)

            renewal_time = now + GmailWatchService.RENEW_BEFORE

            users = (
                db.query(User)
                .filter(
                    User.gmail_watch_expiration.is_not(None),
                    User.gmail_watch_expiration <= renewal_time,
                )
                .all()
            )

            if not users:
                print("No Gmail watches need renewal.")
                return

            print(f"Renewing Gmail watch for {len(users)} user(s)...")

            for user in users:

                try:

                    enable_gmail_watch(
                        db=db,
                        current_user=user,
                    )

                    print(
                        f"Renewed Gmail watch for {user.email}"
                    )

                except Exception as e:

                    print(
                        f"Failed to renew watch for {user.email}: {e}"
                    )

            db.commit()

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()