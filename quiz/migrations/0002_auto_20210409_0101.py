# Generated by Django 3.1.7 on 2021-04-09 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['category'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'get_latest_by': 'pub_date', 'ordering': ['-pub_date', 'title'], 'verbose_name': 'Quiz', 'verbose_name_plural': 'Quizzes'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ['sub_category'], 'verbose_name': 'Sub-Category', 'verbose_name_plural': 'Sub-Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=1, help_text='a user friendly url', max_length=31, unique=True, verbose_name='user friendly url'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='image',
            field=models.ImageField(default='quiz_default.jpg', upload_to='quiz_pic'),
        ),
    ]