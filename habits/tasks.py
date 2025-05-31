from celery import shared_task
from django.utils import timezone


@shared_task()
def send_notification():
    date = timezone.now().today()
    print(date)