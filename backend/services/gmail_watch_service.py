from datetime import datetime, timedelta, timezone
from core.database import SessionLocal
from models.user import User
from services.gmail_service import enable_gmail_watch
# this file renews the gmail watch subscription before it expires

import logging
logger = logging.getLogger(__name__)

class GmailWatchService:

    RENEW_BEFORE = timedelta(days=1) # buffer of 1 day

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
                    User.gmail_watch_expiration <= renewal_time, # if expires today or tommorow renew
                )
                .all()
            )

            if not users:
                logger.info("No Gmail watches need renewal")
                return

            logger.info(
                "Renewing Gmail watch for %d user(s)",
                len(users),
            )

            for user in users:

                try:

                    enable_gmail_watch(
                        db=db,
                        current_user=user,
                    )

                    logger.info(
                        "Renewed Gmail watch for %s",
                        user.email,
                    )

                except Exception:

                    logger.exception(
                        "Failed to renew Gmail watch for %s",
                        user.email,
                    )

            db.commit() # commit once for many users to avoid db overhead

        except Exception:

            db.rollback()
            logger.exception(
                "Gmail watch renewal job failed"
            )
            raise

        finally:

            db.close()