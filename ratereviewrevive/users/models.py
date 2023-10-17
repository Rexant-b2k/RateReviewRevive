from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    BASE_ROLES = ((ADMIN, 'admin'), (MODERATOR, 'moderator'), (USER, 'user'))

    email = models.EmailField(
        max_length=254,
        verbose_name='E-mail',
        unique=True
    )
    username = models.TextField(
        max_length=150,
        verbose_name='Имя',
        unique=True,
        db_index=True,
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )
    role = models.CharField(
        max_length=15,
        verbose_name='Права пользователя',
        choices=BASE_ROLES,
        default=USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
