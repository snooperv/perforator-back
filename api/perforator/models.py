from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User


class PUser(User):
    phone = models.CharField(max_length=12)
    sbis = models.CharField(max_length=255)


class SelfReview(models.Model):
    input_part = models.CharField(max_length=512)
    plans = models.CharField(max_length=512)
    self_review = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
