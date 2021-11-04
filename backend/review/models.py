from ..api.models import Profile
from ..performance_review.models import PerformanceReview
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Модель Ревью (для обычного ревью и селф-ревью)
class Review(models.Model):
    appraising_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='appraising_person')
    evaluated_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='evaluated_person')
    performance_review = models.ForeignKey(PerformanceReview,
                                           on_delete=models.CASCADE,
                                           related_name='performance_review',
                                           default=0)
    is_draft = models.BooleanField(default=True)


# Модель Категория оценки (по которой пользователю предлагают
# оценить сотрудника)
class GradeCategory(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)


# Модель Оценка (непосредственно оценка с комментарием)
class Grade(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    grade_category = models.ForeignKey(GradeCategory, on_delete=models.DO_NOTHING, default=0)
    grade = models.IntegerField(validators=[
        MaxValueValidator(4),
        MinValueValidator(1)
    ], null=True)
    comment = models.CharField(max_length=120)
