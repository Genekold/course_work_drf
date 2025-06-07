from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):
    """Тестирование CRUD привычек."""

    def setUp(self):
        self.user = User.objects.create(
            email="test@skay.pro", password="qwe123", tg_chat_id=1234
        )
        self.other_user = User.objects.create(email="ohter@skay.pro", password="QWE123")
        self.nice_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            start_time="08:00:00",
            action="Массаж головы",
            is_nice=True,
            lead_time=120,
        )
        self.other_nice_habit = Habit.objects.create(
            owner=self.other_user,
            place="Дом",
            start_time="08:00:00",
            action="Поиграть на гитаре",
            is_nice=True,
            lead_time=120,
        )
        self.useful_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            start_time="09:00:00",
            action="Пробежка",
            periodicity="3_DAY",
            reward="Съесть мороженое",
            is_public=True,
        )
        self.useful_habit_2 = Habit.objects.create(
            owner=self.user,
            place="Дом",
            start_time="12:00:00",
            action="Полить цветы",
            periodicity="4_DAY",
            related_habit=self.nice_habit,
        )
        self.other_useful_habit = Habit.objects.create(
            owner=self.other_user,
            place="Дом",
            start_time="21:00:00",
            action="Учить язык python",
            periodicity="1_DAY",
            related_habit=self.other_nice_habit,
        )

        self.list_url = reverse("habits:habit-list")
        self.detail_url = reverse("habits:habit-detail", args=[self.useful_habit.id])

    def test_authentication_required(self):
        """Проверка, что API требует аутентификации."""

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_habits_authenticated(self):
        """Проверка получения списка привычек аутентифицированным пользователем."""

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_other_list_habits_authenticated(self):
        """Проверка получения списка привычек другим аутентифицированным пользователем."""

        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_create_nice_habit(self):
        """Создание приятной привычки."""

        self.client.force_authenticate(user=self.other_user)
        habit = {
            "place": "Дом",
            "start_time": "09:00:00",
            "action": "Постлушать любимую музыку",
            "is_nice": True,
            "periodicity": "1_DAY",
            "lead_time": 120,
        }
        response = self.client.post(self.list_url, habit)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(Habit.objects.get(id=response.data["id"]).reward)

    def test_cant_add_reward_to_pleasant(self):
        """Нельзя добавить вознаграждение к приятной привычке."""
        self.client.force_authenticate(user=self.user)
        data = {"is_nice": True, "reward": "Съесть шоколадку"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "У приятной привычки не может быть ни 'Связаной привычки', ни 'Вознаграждения'",
            str(response.data),
        )

    def test_need_reward_or_related_for_useful(self):
        """У полезной привычки должно быть одно из полей 'Связаная привычка' или 'Вознаграждение'."""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Дом",
            "start_time": "09:00:00",
            "action": "Подтянуться на турнике",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "За выполнение полезной привычки неоходимо себя порадовать и выбрать одно из полей:"
            " 'Связаная привычка' или 'Вознаграждение'",
            str(response.data),
        )

    def test_cant_have_both_reward_and_related(self):
        """Нельзя указать и вознаграждение, и связанную привычку."""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Дом",
            "start_time": "09:00:00",
            "action": "Подтянуться на турнике",
            "reward": "Съесть шоколадку",
            "related_habit": self.nice_habit.pk,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Необходимо выбрать одно из полей: 'Связаная привычка' или 'Вознаграждение', а не оба поля",
            str(response.data),
        )

    def test_cant_have_related_not_nice_habit(self):
        """В связаной привычке нельзя указать привычку без флага 'Приятная'."""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Дом",
            "start_time": "09:00:00",
            "action": "Подтянуться на турнике",
            "related_habit": self.useful_habit.pk,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_habit(self):
        """Обновление привычки."""
        self.client.force_authenticate(user=self.user)
        data = {"action": "Новое действие"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.useful_habit.refresh_from_db()
        self.assertEqual(self.useful_habit.action, "Новое действие")

    def test_delete_habit(self):
        """Удаление привычки."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.useful_habit.id).exists())

    def test_public_habits_visibility(self):
        """Публичные привычки видны всем."""

        self.list_url_public = reverse("habits:habit-public-habit")
        response = self.client.get(self.list_url_public)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
