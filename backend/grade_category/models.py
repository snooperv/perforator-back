from django.db import models
from ..performance_review.models import PerformanceReview


class GradeCategory(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    performance_review = models.ManyToManyField(PerformanceReview)

