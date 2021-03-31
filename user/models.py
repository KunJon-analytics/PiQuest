from django.conf import settings
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.

class User(AbstractUser):
    is_taker = models.BooleanField(default=True)
    is_master = models.BooleanField(default=False)
    email = models.EmailField('email address', max_length=254, unique=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return self.profile.get_absolute_url()

    def get_full_name(self):
        return self.profile.name

    def get_short_name(self):
        return self.profile.name

    def published_quizzes(self):
        return self.quizzes.filter(pub_date__lt=date.today())

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30, unique=True)
    about = models.TextField()
    joined = models.DateTimeField("Date Joined", auto_now_add=True)
    

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return reverse('piquest-auth:public_profile', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('piquest-auth:profile_update')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)




