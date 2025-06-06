from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):
    """Тестирование CRUD привычек"""

    def setUp(self):
        self.user = User.objects.create(
            email="test@skay.pro",
            password="qwe123",
            tg_chat_id=1234
        )
        self.other_user = User.objects.create(
            email="ohter@skay.pro",
            password="QWE123"
        )
        self.nice_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            start_time="08:00:00",
            action="Массаж головы",
            is_nice=True,
            lead_time=120
        )
        self.other_nice_habit = Habit.objects.create(
            owner=self.other_user,
            place="Дом",
            start_time="08:00:00",
            action="Поиграть на гитаре",
            is_nice=True,
            lead_time=120
        )
        self.useful_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            start_time="09:00:00",
            action="Пробежка",
            periodicity="3_DAY",
            reward="Съесть мороженое"
        )
        self.useful_habit_2 = Habit.objects.create(
            owner=self.user,
            place="Дом",
            start_time="12:00:00",
            action="Полить цветы",
            periodicity="4_DAY",
            related_habit=self.nice_habit
        )
        self.other_useful_habit = Habit.objects.create(
            owner=self.other_user,
            place="Дом",
            start_time="21:00:00",
            action="Учить язык python",
            periodicity="1_DAY",
            related_habit=self.nice_habit
        )

        self.list_url = reverse('habits:habit-list')
        self.detail_url = reverse('habits:habit-detail', args=[self.useful_habit.id])

    def test_authentication_required(self):
        """Проверка, что API требует аутентификации."""

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_habits_authenticated(self):
        """Проверка получения списка привычек аутентифицированным пользователем"""

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_other_list_habits_authenticated(self):
        """Проверка получения списка привычек другим аутентифицированным пользователем"""

        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)



