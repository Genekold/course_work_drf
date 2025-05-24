from rest_framework import serializers

from habits.models import Habit
from habits.validators import RewardAndRelatedHabit, ValidationRelatedHabit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки"""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RewardAndRelatedHabit(),
            ValidationRelatedHabit(),
        ]
