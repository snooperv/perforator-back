# Generated by Django 3.2.9 on 2021-12-01 13:08

from django.db import migrations, models
import perforator.models


class Migration(migrations.Migration):

    dependencies = [
        ('perforator', '0012_auto_20211119_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='peers',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='perforator.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(null=True, upload_to=perforator.models.savePhotoUnderRandomName),
        ),
    ]
