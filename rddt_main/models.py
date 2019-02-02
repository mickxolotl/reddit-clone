from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils import timezone


class RedditUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True, verbose_name='Имя пользователя', error_messages={
        'unique': "Пользователь с таким именем уже существует",
    })
    email = models.EmailField(max_length=100, verbose_name='Электронная почта')
    phone_regex = RegexValidator(r'^\+?\d{9,15}$', 'Введите номер телефона в формате +99999999999')
    phone_number = models.CharField(max_length=16, validators=[phone_regex], verbose_name='Номер телефона')
    about = models.TextField(max_length=400, verbose_name='О себе')
    join_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
