from apscheduler.schedulers.background import BackgroundScheduler

from services.notification_service import NotificationService
from services.gmail_watch_service import GmailWatchService
from services.cleanup_service import CleanupService

scheduler = BackgroundScheduler(timezone="UTC")


def start_scheduler():

    scheduler.add_job(
        NotificationService.process_due_reminders,
        trigger="interval",
        minutes=1,
        id="telegram-reminders",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    scheduler.add_job(
        GmailWatchService.renew_expiring_watches,
        trigger="interval",
        hours=24,
        id="gmail-watch-renewal",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    scheduler.add_job(
        CleanupService.cleanup,
        trigger="interval",
        minutes=10,
        id="cleanup-job",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    print("✅ Reminder Scheduler Started")