from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send_daily_user_report': {
        'task': 'core.tasks.send_daily_user_report',
        'schedule': crontab(hour='0', minute='0'),
    },
}
