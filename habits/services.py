from datetime import datetime
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
    habits_1_day = habits.filter(periodicity="1_DAY")
    habits_1_day.update(next_execution=(now + timedelta(days=1)))
    habits_1_day = habits.filter(periodicity="2_DAY")
    habits_1_day.update(next_execution=(now + timedelta(days=2)))
    habits_1_day = habits.filter(periodicity="3_DAY")
    habits_1_day.update(next_execution=(now + timedelta(days=3)))
    habits_1_day = habits.filter(periodicity="4_DAY")
    habits_1_day.update(next_execution=(now + timedelta(days=4)))
    habits_1_day = habits.filter(periodicity="5_DAY")
    habits_1_day.update(next_execution=(now + timedelta(days=5)))
    habits_1_day = habits.filter(periodicity="6_DAY")
    habits_1_day.update(next_execution=(now + timedelta(days=6)))
    habits_1_day = habits.filter(periodicity="7_DAY")
    habits_1_day.update(next_execution=(now + timedelta(days=7)))


def set_sending_time(time: str):
    """Устанавливает время отправки сообщенияю."""

    now_date = timezone.now().date()
    date_str = f"{now_date} {time}"
    send_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") - timedelta(minutes=5)
    return send_date
