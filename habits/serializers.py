from rest_framework import serializers

from habits.models import Habit
from habits.validators import RewardAndRelatedHabit, ValidationRelatedHabit
from users.models import User


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки"""

    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RewardAndRelatedHabit(),
            ValidationRelatedHabit(),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for validator in self.validators:
            if hasattr(validator, "set_instance"):
                validator.set_instance(self.instance)
