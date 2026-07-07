from services.gmail_service import GmailService
from services.parser_service import ParserService
from services.preprocessor_service import PreprocessorService
from services.filter_service import FilterService
from services.analysis_service import AnalysisService
from services.email_service import EmailService
from services.reminder_service import ReminderService
from core.security import Security
from services.spam_service import SpamService

class SyncService:

    @staticmethod
    def sync_user(db, user):

        try:
            refresh_token = Security.decrypt(
                user.encrypted_refresh_token
            )

            result = GmailService.sync(
                refresh_token=refresh_token,
                last_history_id=user.last_history_id,
            )

            

            emails = result["emails"]
            latest_history_id = result["latest_history_id"]

            for raw_email in emails:

                parsed = ParserService.parse(raw_email)

                parsed["body"] = PreprocessorService.clean(
                    parsed["body"]
                )

                should_continue = FilterService.should_continue(
                    parsed["subject"],
                    parsed["body"],
                )

                if not should_continue:
                    continue

                likely_spam = SpamService.predict(
                    parsed["body"]
                )

                analysis = AnalysisService.analyze(
                    subject=parsed["subject"],
                    body=parsed["body"],
                    received_at=parsed["received_at"],
                    likely_spam=likely_spam
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

            # Every Gmail message has now been processed
            user.last_history_id = latest_history_id

            db.commit()

        except Exception:

            db.rollback()

            raise