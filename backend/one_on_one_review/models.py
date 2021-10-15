from django.db import models
from ..profile.models import Profile


class OneOnOneReview(models.Model):
    common_note = models.CharField(max_length=360)
    manager_note = models.CharField(max_length=360)
    subordinate_note = models.CharField(max_length=360)
    manager = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='one_on_one_reviews_manager')
    subordinate = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='one_on_one_reviews_subordinate')

