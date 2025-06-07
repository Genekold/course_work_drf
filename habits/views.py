from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginations import Pagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitsViewSet(ModelViewSet):
    """Представление привычки"""

    serializer_class = HabitSerializer
    pagination_class = Pagination
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Собираем только привычки текущего пользователя
        return Habit.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Поле 'owner' заполняем авторизованым пользователем.
        serializer.save(owner=self.request.user)

    @action(
        detail=False,
        methods=["get"],
        pagination_class=Pagination,
        url_name="public-habit",
        url_path="public-habit",
        permission_classes=[AllowAny],
    )
    def public(self, request):
        # Получение списка публичных привычек

        qs = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
