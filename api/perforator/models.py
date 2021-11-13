from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


# Модель Профиль (связан с User джанги 1-к-1)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    sbis = models.CharField(max_length=128)
    peers = models.ManyToManyField('self', default=None, blank=True, null=True)
    photo = models.CharField(max_length=32, default=None, blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class SelfReview(models.Model):
    input_part = models.CharField(max_length=512)
    plans = models.CharField(max_length=512)
    self_review = models.ForeignKey(User, on_delete=models.CASCADE)


# Модель Категория оценки (по которой пользователю предлагают
# оценить сотрудника)
class GradeCategory(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)


# Модель Перформанс-Ревью
class PerformanceReview(models.Model):
    self_review_categories = models.ManyToManyField(GradeCategory, related_name='self_review_categories', default=None)
    manager_review_categories = models.ManyToManyField(GradeCategory, related_name='manager_review_categories', default=None)
    peers_review_categories = models.ManyToManyField(GradeCategory, related_name='peers_review_categories', default=None)
    team_review_categories = models.ManyToManyField(GradeCategory, related_name='team_review_categories', default=None)


# Модель Ревью (для обычного ревью и селф-ревью. В случае последнего в оценках числовое значение остаётся null)
class Review(models.Model):
    appraising_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='appraising_person')
    evaluated_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='evaluated_person')
    performance_review = models.ForeignKey(PerformanceReview,
                                           on_delete=models.CASCADE,
                                           related_name='performance_review',
                                           default=0)
    is_draft = models.BooleanField(default=True)
    is_not_enough_data = models.BooleanField(default=False)


# Модель Оценка (непосредственно оценка с комментарием. Null в числе для селф-ревью.)
class Grade(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    grade_category = models.ForeignKey(GradeCategory, on_delete=models.DO_NOTHING, default=0)
    grade = models.IntegerField(validators=[
        MaxValueValidator(4),
        MinValueValidator(1)
    ], null=True)
    comment = models.CharField(max_length=120)


# Модель Средняя Оценка (на будущее)
class AverageGrade(models.Model):
        performance_review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE)
        evaluated_person = models.ForeignKey(Profile, on_delete=models.CASCADE)
        grade_category = models.ForeignKey(GradeCategory, on_delete=models.PROTECT)
        raw_grade = models.FloatField()
        normalized_grade = models.FloatField()