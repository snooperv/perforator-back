from ..profile.models import Profile
from django.db import models

from ..grade_category.models import GradeCategory
from ..performance_review.models import PerformanceReview


class AverageGrade(models.Model):
    performance_review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE)
    evaluated_person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    grade_category = models.ForeignKey(GradeCategory, on_delete=models.PROTECT)
    raw_grade = models.FloatField()
    normalized_grade = models.FloatField()
