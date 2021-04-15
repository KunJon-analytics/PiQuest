# Generated by Django 3.1.7 on 2021-04-09 00:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0002_auto_20210409_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articlelink',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='projects.project'),
        ),
        migrations.AddField(
            model_name='articlelink',
            name='quiz',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz'),
        ),
        migrations.AlterUniqueTogether(
            name='articlelink',
            unique_together={('slug', 'project')},
        ),
    ]