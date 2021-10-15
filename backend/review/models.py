from ..profile.models import Profile
from django.db import models

from ..performance_review.models import PerformanceReview


class Review(models.Model):
    appraising_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='appraising_person')
    evaluated_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='evaluated_person')
    performance_review = models.ForeignKey(PerformanceReview,
                                           on_delete=models.CASCADE,
                                           related_name='performance_review',
                                           default=0)
    is_draft = models.BooleanField(default=True)
