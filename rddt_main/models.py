from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils import timezone
from . import utils


class RedditUser(AbstractBaseUser):
    username_regex = RegexValidator(r'^[\dA-zА-я_\-\.]+$',
                                    'Имя пользователя должно состоять из цифр, латиницы, кириллицы или знаков "_-."')
    username = models.CharField(max_length=30, unique=True, validators=[username_regex],
                                verbose_name='Имя пользователя', error_messages={
        'unique': "Пользователь с таким именем уже существует",
    })
    email = models.EmailField(max_length=100, verbose_name='Электронная почта', blank=True)
    phone_regex = RegexValidator(r'^\+?\d{9,15}$', 'Введите номер телефона в формате +99999999999')
    phone_number = models.CharField(max_length=16, validators=[phone_regex], verbose_name='Номер телефона')
    about = models.TextField(max_length=400, verbose_name='О себе', blank=True)
    join_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Post(models.Model):
    author = models.ForeignKey(RedditUser, models.CASCADE)
    publish_date = models.DateTimeField(default=timezone.now)
    text = models.TextField(max_length=5000, verbose_name='Текст')

    class Meta:
        ordering = ('-publish_date', )

    @property
    def root_comments(self):
        return self.comment_set.filter(replied_comment=None)

    @property
    def comments_count_sign(self):
        comments_count = self.comment_set.count()
        return utils.plural_form(comments_count, ('комментарий', 'комментария', 'комментариев'))


class Comment(models.Model):
    author = models.ForeignKey(RedditUser, models.CASCADE)
    publish_date = models.DateTimeField(default=timezone.now)
    text = models.TextField(max_length=1000)
    replied_post = models.ForeignKey(Post, models.CASCADE)
    replied_comment = models.ForeignKey('self', models.CASCADE, default=None, null=True, blank=True)

    class Meta:
        ordering = ('publish_date', )

    @property
    def root_comments(self):
        return self.comment_set.all
