from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from config import settings


class Habit(models.Model):
    """Модель привычки."""

    PERIODICITY_TYPE = [
        ("1_DAY", "Ежедневно"),
        ("2_DAY", "Каждые 2 дня"),
        ("3_DAY", "Каждые 3 дня"),
        ("4_DAY", "Каждые 4 дня"),
        ("5_DAY", "Каждые 5 дней"),
        ("6_DAY", "Каждые 6 дней"),
        ("7_DAY", "Каждые 7 дней"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Автор привычки",
        help_text="Введите автора привычки",
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    next_execution = models.DateField(
        blank=True, null=True, verbose_name="Дата следующего выполнения"
    )
    place = models.CharField(
        max_length=200,
        verbose_name="Место выполнения",
        help_text="Укажите место выполнения",
    )
    start_time = models.TimeField(
        verbose_name="Время начала выполнения привычки",
        help_text="Укажите время, когда необходимо выполнить привычку",
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие привычки",
        help_text="Укажите действие привычки",
    )
    is_nice = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Укажите, является ли привычка приятной",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="habit",
        limit_choices_to={"is_nice": True},
        verbose_name="Связанная привычка",
        help_text="Укажите связаную приятную привычку",
    )
    periodicity = models.CharField(
        max_length=5,
        choices=PERIODICITY_TYPE,
        default="1_DAY",
        verbose_name="Периодичность выполнения",
        help_text="Укажите тип периодичности выполнения",
    )
    reward = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Укажите вознаграждение за выполнение полезной привычки",
    )
    lead_time = models.PositiveIntegerField(
        default=60,
        verbose_name="Время выполнения",
        help_text="Время необходимое для пыполнения привычки",
        validators=[MinValueValidator(10), MaxValueValidator(120)],
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text="Укажите можно ли показывать привычку в общий доступ.",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = [
            "start_time",
        ]

    def __str__(self):
        return f"{self.action} в {self.start_time}, {self.place}"
