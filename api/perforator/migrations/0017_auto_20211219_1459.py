# Generated by Django 3.1.7 on 2021-12-19 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perforator', '0016_auto_20211209_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peerreviews',
            name='rates_deadlines',
            field=models.IntegerField(choices=[(1, 'Lower'), (2, 'Low'), (3, 'High'), (4, 'Higher')]),
        ),
        migrations.CreateModel(
            name='OneToOneReviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_notes', models.CharField(max_length=2048)),
                ('manager_notes', models.CharField(max_length=2048)),
                ('employee_notes', models.CharField(max_length=2048)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_reviews', to='perforator.profile')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager_reviews', to='perforator.profile')),
            ],
        ),
    ]
