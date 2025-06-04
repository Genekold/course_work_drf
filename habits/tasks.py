from celery import shared_task

from habits.services import get_habits_for_today, set_next_date_execution, set_sending_time, send_telegram_message
from users.models import User


@shared_task()
def queue_send_message(chat_id, message):
    """Выполняет отправку уведомления"""
    send_telegram_message(chat_id, message)


@shared_task()
def send_notification():
    """Определяет привычки для отправки уведомлений"""
    habits = get_habits_for_today()

    if habits:
        for habit in habits:
            chat_id = habit.owner.tg_chat_id
            message = f"Через 5 мининут {habit.place} выполнить {habit.action}"
            time_send = set_sending_time(habit.start_time)
            queue_send_message.apply_async(args=[chat_id, message], eta=time_send)
            print(time_send)
    else:
        for user in User.objects.exclude(is_superuser=True):
            chat_id = user.tg_chat_id
            message = "Сегодня не запланированы привычки"
            time_send = "11:21:00"
            time_send = set_sending_time(time_send)
            queue_send_message.apply_async(args=[chat_id, message], eta=time_send)

    set_next_date_execution(habits)
