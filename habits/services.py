from datetime import timedelta

import requests
from django.utils import timezone

from config import settings
from habits.models import Habit


def send_telegram_message(chat_id, message):
    """Функция для отправки уведомления на телеграмм"""

    params = {
        'text': message,
        'chat_id': chat_id,
    }

    requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage', params=params)


def get_habits_for_today():
    """Для привычек созданых за последние 24 часа устанавливает дату выполнения и выбирает привычки на сегодня."""
    now = timezone.now()
    last_24_hour = now - timedelta(hours=24)
    habits = Habit.objects.filter(created_at__gte=last_24_hour)
    habits.update(next_execution=now.date())
    return Habit.objects.filter(next_execution=now).filter(is_nice=False)


def set_next_date_execution(habits):
    """Устанавливает дату следующего выполнения."""
    now = timezone.now()
    habits_1_day = habits.filter(periodicity="1DAY")
    habits_1_day.update(next_execution=(now + timedelta(days=1)))
