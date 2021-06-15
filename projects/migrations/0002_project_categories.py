# Generated by Django 3.0.7 on 2021-06-10 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='projects', to='quiz.Category'),
        ),
    ]
