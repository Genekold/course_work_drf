from celery import shared_task

from habits.services import get_habits_for_today, set_next_date_execution


@shared_task()
def send_notification():
    habits = get_habits_for_today()
    for habit in habits:
        chat_id = habit.owner.tg_chat_id
        message = f"Через 5 мининут {habit.place} выполнить {habit.action}"

    set_next_date_execution(habits)
