from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    sbis = models.CharField(max_length=255)
    password = models.CharField(max_length=32)
