from celery import Celery
from celery.schedules import crontab
from backend.core.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
    beat_schedule={
        "cleanup-expired-sessions": {
            "task": "backend.tasks.cleanup.cleanup_expired_sessions",
            "schedule": crontab(minute="0", hour="*/1"),  # Every hour
        },
        "cleanup-pending-payments": {
            "task": "backend.tasks.cleanup.cleanup_pending_payments",
            "schedule": crontab(minute="30", hour="*/1"),  # Every hour at :30
        },
        "cleanup-expired-subscriptions": {
            "task": "backend.tasks.cleanup.cleanup_expired_subscriptions",
            "schedule": crontab(minute="0", hour="0"),  # Daily at midnight
        },
        "validate-with-stripe": {
            "task": "backend.tasks.cleanup.validate_with_stripe",
            "schedule": crontab(minute="15", hour="*/2"),  # Every 2 hours at :15
        },
    },
)

celery_app.autodiscover_tasks(["backend.tasks"])
