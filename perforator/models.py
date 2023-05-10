import os
from uuid import uuid4
from django.db import models
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


class Companies(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, default=None)


class PerformanceProcess(models.Model):
    """
    status: 0 - Performance review окончено; 1 - этап self-review
            2 - этап утверждения пиров; 3 - этап оценивания друг друга
            4 - этап one to one
    """
    is_active = models.BooleanField(default=False)
    status = models.IntegerField(default=0)
    deadline = models.DateTimeField(auto_now=False)


# Модель Профиль (связан с User джанги 1-к-1)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    sbis = models.CharField(max_length=128)
    peers = models.ManyToManyField('self', symmetrical=False, default=None, blank=True,
                                   related_name='i_am_peer_to')
    photo = models.ImageField(null=True, upload_to=savePhotoUnderRandomName)
    approve = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    team_id = models.IntegerField(default=0, null=True)
    pr = models.IntegerField(default=-1, null=True)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)

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


class Team(models.Model):
    manager = models.ForeignKey(Profile, on_delete=models.CASCADE)


class PrList(models.Model):
    """
    """
    pr = models.ForeignKey(PerformanceProcess, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    is_active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=False)


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


class Questionary(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    perforator = models.ForeignKey(PerformanceProcess, on_delete=models.CASCADE)
    mark_system = models.IntegerField(default=-1, null=True)
    is_self_review = models.BooleanField(default=False)


# Модель Ревью (для обычного ревью и селф-ревью. В случае последнего в оценках числовое значение остаётся null)
class Review(models.Model):
    appraising_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='appraising_person')
    evaluated_person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='evaluated_person')
    questionary = models.ForeignKey(Questionary, on_delete=models.CASCADE, default=None)
    is_draft = models.BooleanField(default=True)
    pr_id = models.IntegerField(default=-1)
    is_self_review = models.BooleanField(default=False)


class Question(models.Model):
    questionary = models.ForeignKey(Questionary, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)


class Answer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, default=None)
    text = models.CharField(max_length=512)
    mark = models.IntegerField(default=-1)


class Tokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_f = models.CharField(max_length=256)
    token_b = models.CharField(max_length=256)
    time_f = models.DateTimeField(null=True, default=None)
    time_b = models.DateTimeField(null=True, default=None)


class UserRating(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pr = models.ForeignKey(PrList, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    manager_mark = models.FloatField(default=-1)
    peer_mark = models.FloatField(default=-1)
    average_mark = models.FloatField(default=-1)


class TeamRating(models.Model):
    manager = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pr = models.ForeignKey(PrList, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    average_mark = models.FloatField(default=-1)
