# Generated by Django 3.1.7 on 2021-04-09 00:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import re


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20210409_0101'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0002_auto_20210409_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='master',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='user.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='number_of_winners',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='quizzes', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='pub_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='reward',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='quizzes', to='quiz.Category'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='slug',
            field=models.SlugField(default=1, help_text='a user friendly url', max_length=31, unique=True, verbose_name='user friendly url'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(blank=True, max_length=31, null=True, unique=True, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='score',
            field=models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Score'),
        ),
        migrations.RemoveField(
            model_name='question',
            name='sub_category',
        ),
        migrations.AddField(
            model_name='question',
            name='sub_category',
            field=models.ManyToManyField(blank=True, related_name='question', to='quiz.SubCategory', verbose_name='Sub-Category'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='draft',
            field=models.BooleanField(blank=True, default=False, help_text='If yes, the quiz is not displayed in the quiz list and can only be taken by users who can edit quizzes.', verbose_name='Draft'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='incorrect_questions',
            field=models.CharField(blank=True, max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Incorrect questions'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='question_list',
            field=models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Question List'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='question_order',
            field=models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Question Order'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='sub_category',
            field=models.CharField(blank=True, max_length=31, null=True, unique=True, verbose_name='Sub-Category'),
        ),
    ]