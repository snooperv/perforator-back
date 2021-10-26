from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User


class User(AbstractUser):
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=12, unique=True)
    sbis = models.CharField(max_length=255)
    password = models.CharField(max_length=32)
    is_superuser = True
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manager = models.OneToOneField('self', on_delete=models.PROTECT)
    peers = models.ManyToManyField('self')
    team = models.ManyToManyField('self')
    phone = models.CharField(max_length=12)


class SelfReview(models.Model):
    introduction = models.CharField(verbose_name="Вводная часть", max_length=512)
    successes = models.CharField(verbose_name="Успехи", max_length=512)
    evolution = models.CharField(verbose_name="Зоны роста", max_length=512)
    plans = models.CharField(verbose_name="Планы на будущее", max_length=512)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

"""
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
"""