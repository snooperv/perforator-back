from django.db import models
from ..api.models import Profile
from ..review.models import GradeCategory

class PerformanceReview(models.Model):
    self_review_categories = models.ManyToManyField(GradeCategory)
    manager_review_categories = models.ManyToManyField(GradeCategory)
    peers_review_categories = models.ManyToManyField(GradeCategory)
    team_review_categories = models.ManyToManyField(GradeCategory)

class AverageGrade(models.Model):
    performance_review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE)
    evaluated_person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    grade_category = models.ForeignKey(GradeCategory, on_delete=models.PROTECT)
    raw_grade = models.FloatField()
    normalized_grade = models.FloatField()