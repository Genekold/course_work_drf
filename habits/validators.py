from django.core.validators import ValidationError


class RewardAndRelatedHabit:
    """Валидация добавления к привычке Связанной привычки или Вознаграждения."""

    def set_instance(self, instance):
        self.instance = instance

    def __call__(self, habit):
        instance = self.instance if hasattr(self, 'instance') else None
        reward = habit.get("reward")
        related_habit = habit.get("related_habit")
        is_nice = habit.get("is_nice", getattr(instance, "is_nice", False)) if instance else habit.get("is_nice", False)

        # если есть экземпляр определяем поля
        current_reward = getattr(instance, 'reward', None) if instance else None
        current_related_habit = getattr(instance, 'related_habit', None) if instance else None

        # окончательные поля для проверки
        final_reward = reward if reward is not None else current_reward
        final_related_habit = related_habit if related_habit is not None else current_related_habit

        if not is_nice and not final_reward and not final_related_habit:
            raise ValidationError(
                "За выполнение полезной привычки неоходимо себя порадовать и выбрать одно из полей:"
                " 'Связаная привычка' или 'Вознаграждение'"
            )

        if is_nice and (final_reward or final_related_habit):
            raise ValidationError(
                "У приятной привычки не может быть ни 'Связаной привычки', ни 'Вознаграждения'"
            )

        if final_reward and final_related_habit:
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
