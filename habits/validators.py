from django.core.validators import ValidationError


class RewardAndRelatedHabit:
    """Валидация добавления к привычке Связанной привычки или Вознаграждения."""

    def __call__(self, habit):

        is_nice = habit.get("is_nice")
        reward = habit.get("reward")
        related_habit = habit.get("related_habit")

        if not is_nice and not reward and not related_habit:
            raise ValidationError(
                "За выполнение полезной привычки неоходимо себя порадовать и выбрать одно из полей:"
                " 'Связаная привычка' или 'Вознаграждение'"
            )

        if is_nice and (reward or related_habit):
            raise ValidationError(
                "У приятной привычки не может быть ни 'Связаной привычки', ни 'Вознаграждения'"
            )

        if reward and related_habit:
            raise ValidationError(
                "Необходимо выбрать одно из полей: 'Связаная привычка' или 'Вознаграждение', а не оба поля"
            )


class ValidationRelatedHabit:
    """Валидация приятности связанной привычки."""

    def __call__(self, habit):
        related_habit = habit.get("related_habit")
        if related_habit and not related_habit.is_nice:
            raise ValidationError(
                "В связанные привычки можно добавит только приятные привычки"
            )
