# Generated by Django 3.0.7 on 2021-06-15 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='about',
            field=models.TextField(default='A brief description about me'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(help_text='Your full name', max_length=255),
        ),
    ]
