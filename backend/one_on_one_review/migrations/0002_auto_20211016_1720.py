# Generated by Django 2.1.4 on 2021-10-16 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one_on_one_review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oneononereview',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
