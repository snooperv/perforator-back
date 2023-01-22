import os
import django.utils.timezone
from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from PIL import Image


def savePhotoUnderRandomName(instance, filename):
    upload_to = 'photos'
    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class SelfReview(models.Model):
    input_part = models.CharField(max_length=512)
    plans = models.CharField(max_length=512)
    self_review = models.ForeignKey(User, on_delete=models.CASCADE)


class PerformanceProcess(models.Model):
    """
    status: 0 - Performance review окончено; 1 - этап self-review
            2 - этап утверждения пиров; 3 - этап оценивания друг друга
            4 - этап one to one
    """
    is_active = models.BooleanField(default=False)
    status = models.IntegerField(default=0)
    deadline = models.DateTimeField(auto_now=False)
    #self_review = models.ForeignKey(SelfReview, on_delete=models.CASCADE, null=True)


class PrList(models.Model):
    """
    """
    pr = models.ForeignKey(PerformanceProcess, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=False)


# Модель Профиль (связан с User джанги 1-к-1)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    sbis = models.CharField(max_length=128)
    #manager = models.ForeignKey('self', on_delete=models.PROTECT, null=True, related_name='team')
    peers = models.ManyToManyField('self', symmetrical=False, default=None, blank=True,
                                   related_name='i_am_peer_to')
    photo = models.ImageField(null=True, upload_to=savePhotoUnderRandomName)
    approve = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    team_id = models.IntegerField(default=0, null=True)
    pr = models.IntegerField(default=-1, null=True)

    def save(self, *args, **kwargs):
        if not self.id and not self.photo:
            return
        super(Profile, self).save(*args, **kwargs)
        image = Image.open(self.photo)
        (width, height) = image.size
        "Max width and height 500"
        if height > width > 500 or height > 500:
            factor = 500 / height
        else:
            factor = 500 / width
        size = (int(width * factor), int(height * factor))
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.photo.path)


class PeerReviews(models.Model):
    """
    peer_id - тот, кто оценивают
    rated_person - тот, кого оценивает
    """
    class Rates(models.IntegerChoices):
        LOWER = 1
        LOW = 2
        HIGH = 3
        HIGHER = 4

    peer_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rated_reviews')
    rated_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='my_reviews')
    deadlines = models.CharField(max_length=512)
    approaches = models.CharField(max_length=512)
    teamwork = models.CharField(max_length=512)
    practices = models.CharField(max_length=512)
    experience = models.CharField(max_length=512)
    adaptation = models.CharField(max_length=512)
    rates_deadlines = models.IntegerField(choices=Rates.choices)
    rates_approaches = models.IntegerField(choices=Rates.choices)
    rates_teamwork = models.IntegerField(choices=Rates.choices)
    rates_practices = models.IntegerField(choices=Rates.choices)
    rates_experience = models.IntegerField(choices=Rates.choices)
    rates_adaptation = models.IntegerField(choices=Rates.choices)
    rates_date = models.DateTimeField(null=True, default=None)
    pr_id = models.IntegerField(default=-1, null=True)


class OneToOneReviews(models.Model):
    manager = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='manager_reviews')
    employee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='employee_reviews')
    common_notes = models.CharField(max_length=2048)
    manager_notes = models.CharField(max_length=2048)
    employee_notes = models.CharField(max_length=2048)
    pr_id = models.IntegerField(default=-1, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Модель Категория оценки (по которой пользователю предлагают
# оценить сотрудника)
class GradeCategory(models.Model):
    name = models.CharField(max_length=64, null=True)
    preview_description = models.CharField(max_length=512, null=True)
    description = models.CharField(max_length=512, null=True)


# Модель Перформанс-Ревью
class PerformanceReview(models.Model):
    self_review_categories = models.ManyToManyField(GradeCategory, related_name='self_review_categories', default=None)
    manager_review_categories = models.ManyToManyField(GradeCategory, related_name='manager_review_categories',
                                                       default=None)
    peers_review_categories = models.ManyToManyField(GradeCategory, related_name='peers_review_categories',
                                                     default=None)
    team_review_categories = models.ManyToManyField(GradeCategory, related_name='team_review_categories', default=None)
    #performance_review_id = models.IntegerField(default=-1)


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
    pr_id = models.IntegerField(default=-1)


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


class Tokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_f = models.CharField(max_length=256)
    token_b = models.CharField(max_length=256)
    time_f = models.DateTimeField(null=True, default=None)
    time_b = models.DateTimeField(null=True, default=None)


class Team(models.Model):
    manager = models.ForeignKey(Profile, on_delete=models.CASCADE)
    test = models.BooleanField(default=False)

