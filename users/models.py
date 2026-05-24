from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Убираем обязательность поля username для авторизации по email
    username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Имя пользователя"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта"
    )

    # Дополнительные поля согласно ТЗ
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар (изображение)"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Номер телефона"
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Страна"
    )

    # Меняем поле для авторизации на email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email
