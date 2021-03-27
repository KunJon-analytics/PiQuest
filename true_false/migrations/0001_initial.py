# Generated by Django 3.1.7 on 2021-03-27 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0002_auto_20210327_0505'),
    ]

    operations = [
        migrations.CreateModel(
            name='TF_Question',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.question')),
                ('correct', models.BooleanField(default=False, help_text='Tick this if the question is true. Leave it blank for false.', verbose_name='Correct')),
            ],
            options={
                'verbose_name': 'True/False Question',
                'verbose_name_plural': 'True/False Questions',
                'ordering': ['category'],
            },
            bases=('quiz.question',),
        ),
    ]
