import logging

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

User = get_user_model()


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_confirmation_email(self, user_email, activation_link):
    try:
        email = EmailMessage(
            f'Confirmation email',
            f'Confirm your email: {activation_link}',
            to=[user_email]
        )
        email.send()
    except MaxRetriesExceededError:
        logging.error('Max retries exceeded for send_confirmation_email task')
    except Exception as exc:
        logging.exception(exc)
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_daily_user_report(self):
    active_users = User.objects.filter(is_active=True)
    user_list = "\n".join([user.username for user in active_users])
    try:
        email = EmailMessage(
            'Daily User Report',
            f'Active Users:\n{user_list}',
            to=['admin@example.com']
        )
        email.send()
    except MaxRetriesExceededError:
        logging.error('Max retries exceeded for send_confirmation_email task')
    except Exception as exc:
        logging.exception(exc)
        raise self.retry(exc=exc)
