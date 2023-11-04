import logging

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.core.mail import EmailMessage


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
