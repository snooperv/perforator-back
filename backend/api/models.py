from django.db import models
from django.contrib.auth.models import User


# модель, созданная Вадимом
class User(models.Model):
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    sbis = models.CharField(max_length=255)
    password = models.CharField(max_length=32)
    token = models.CharField(max_length=128, default=None, blank=True, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manager = models.OneToOneField('self', on_delete=models.PROTECT)
    peers = models.ManyToManyField('self')
    team = models.ManyToManyField('self')
    photo = models.CharField(max_length=32, default=None, blank=True, null=True)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
