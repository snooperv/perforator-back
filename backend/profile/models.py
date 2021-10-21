from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manager = models.OneToOneField('self', on_delete=models.PROTECT)
    peers = models.ManyToManyField('self')
    team = models.ManyToManyField('self')
    phone = models.CharField(max_length=12)
    photo = models.UUIDField(null=True)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
