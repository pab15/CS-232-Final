# Generated by Django 3.0.5 on 2020-05-03 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='workouts',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='workouts',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
