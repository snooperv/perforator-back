from django.db import models

from ..grade_category.models import GradeCategory
from ..review.models import Review
from django.core.validators import MinValueValidator, MaxValueValidator


class Grade(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    grade_category = models.ForeignKey(GradeCategory, on_delete=models.DO_NOTHING, default=0)
    grade = models.IntegerField(validators=[
        MaxValueValidator(4),
        MinValueValidator(1)
    ])
    comment = models.CharField(max_length=120)
