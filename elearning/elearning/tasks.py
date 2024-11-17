from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage
@shared_task
def send_email_thread(subject, body, subscriber):
    email = EmailMessage(subject, body, to=[subscriber.email])
    email.send()