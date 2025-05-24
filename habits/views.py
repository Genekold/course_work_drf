from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginations import Pagination
from habits.serializers import HabitSerializer


class HabitsViewSet(ModelViewSet):
    """Представление привычки"""

    serializer_class = HabitSerializer
    pagination_class = Pagination

    def get_queryset(self):
        # Собираем только привычки текущего пользователя
        return Habit.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Поле 'owner' заполняем авторизованым пользователем.
        serializer.save(owner=self.request.user)
