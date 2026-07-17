from apscheduler.schedulers.background import BackgroundScheduler

from services.notification_service import NotificationService
from services.gmail_watch_service import GmailWatchService
from services.cleanup_service import CleanupService

scheduler = BackgroundScheduler(timezone="UTC") # it runs in a separate background thread while Fastapi continues serving requests


def start_scheduler():

    scheduler.add_job(
        NotificationService.process_due_reminders, # passing func reference not calling it immedieately
        trigger="interval", # run repeatedly, not once
        minutes=1,
        id="telegram-reminders", # unique identifier
        replace_existing=True, # in case 2 identical jobs are there, only one would work
        max_instances=1, # if prev run is still active, not start other
        coalesce=True, # it combines missed execution into one
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

    scheduler.start() # it starts scheduler , above only registration 

    print("✅ Reminder Scheduler Started")