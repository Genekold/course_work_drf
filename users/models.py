from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель поьзователя"""

    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    tg_chat_id = models.CharField(
        max_length=50,
        verbose_name="Чат ID в телеграмм",
        help_text="Укажите чат ID в телеграмм",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
