from services.gmail_service import GmailService
from services.parser_service import ParserService
from services.preprocessor_service import PreprocessorService
from services.filter_service import FilterService
from services.analysis_service import AnalysisService
from services.email_service import EmailService
from services.reminder_service import ReminderService
from core.security import Security
from services.spam_service import SpamService
# this is the pipeline which connects services

import logging
logger = logging.getLogger(__name__)

class SyncService:

    @staticmethod
    def sync_user(db, user):

        try:
            logger.info(
                "Starting Gmail sync for user %s",
                user.email,
            )
            refresh_token = Security.decrypt( # get the decrypted refresh token
                user.encrypted_refresh_token
            )

            result = GmailService.sync( # it will make mails in sync by decideing either initial or incremental sync
                refresh_token=refresh_token,
                last_history_id=user.last_history_id,
            )

            

            emails = result["emails"]
            latest_history_id = result["latest_history_id"]

            logger.info(
                "Fetched %d email(s) for user %s",
                len(emails),
                user.email,
            )

            for raw_email in emails:

                parsed = ParserService.parse(raw_email) # raw gmail json to python dict

                parsed["body"] = PreprocessorService.clean( # cleaner text for llm
                    parsed["body"]
                )

                likely_spam = SpamService.predict(
                    parsed["body"]
                )

                should_continue = FilterService.should_continue( # llm decision
                    parsed["subject"],
                    parsed["body"],
                    likely_spam=likely_spam
                )

                if not should_continue:
                    logger.info(
                        "Skipped email %r for user %s",
                        parsed["subject"],
                        user.email,
                    )
                    continue

                

                analysis = AnalysisService.analyze(
                    subject=parsed["subject"],
                    body=parsed["body"],
                    received_at=parsed["received_at"]
                )

                email = EmailService.create(
                    db=db,
                    user_id=user.id,
                    parsed_email=parsed,
                    analysis=analysis,
                )

                ReminderService.create(
                    db=db,
                    email=email,
                )
                logger.info(
                    "Processed email %r for user %s",
                    parsed["subject"],
                    user.email,
                )

            # every Gmail message has now been processed so update latest history id
            user.last_history_id = latest_history_id
            
            db.commit()
            logger.info(
                "Completed Gmail sync for user %s",
                user.email,
            )

        except Exception:
            db.rollback()
            logger.exception(
                "Gmail sync failed for user %s",
                user.email,
            )
            raise