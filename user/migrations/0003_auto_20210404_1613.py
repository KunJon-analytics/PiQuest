# Generated by Django 3.1.7 on 2021-04-04 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210403_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_default.jpg', upload_to='profile_pics'),
        ),
    ]
