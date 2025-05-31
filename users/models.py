from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель поьзователя"""

    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    tg_chat_id = models.CharField(
        unique=True,
        max_length=50,
        verbose_name="chat-id в телеграмм",
        help_text="Укажите chat-id в телеграмм"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
