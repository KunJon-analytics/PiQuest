# Generated by Django 3.0.7 on 2021-10-26 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20210930_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='winner',
            name='claimed',
            field=models.BooleanField(default=False),
        ),
    ]
