from django.conf import settings
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from datetime import date
import pywaves as pw

# Create your models here.

WART = "4kXACcTnNJa14Zbs19irgg48G6jR5nWp8SgPndFWY5av" 
piquestsAddress = pw.Address(privateKey=settings.PIQUESTS_PK)
WART_ASSET = pw.Asset('4kXACcTnNJa14Zbs19irgg48G6jR5nWp8SgPndFWY5av')

class User(AbstractUser):
    is_taker = models.BooleanField(default=True)
    is_master = models.BooleanField(default=False)
    is_project_manager = models.BooleanField(default=False)
    email = models.EmailField('email address', max_length=254, unique=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return self.profile.get_absolute_url()

    def get_full_name(self):
        return self.profile.name

    def get_short_name(self):
        return self.profile.name

    def get_wallet_balance(self):
        try:
            userAddress = pw.Address(self.profile.wallet_address)
            return int(userAddress.balance(WART))/10**8
        except ValueError:
                return -1
        

    def get_image_url(self):
        return self.profile.image.url

    def published_quizzes(self):
        return self.quizzes.filter(pub_date__lt=date.today())

    def get_projects(self):
        return self.projects.all()

    def completed_sittings(self):
        return self.sittings.filter(complete=True)

    def total_sittings(self):
        return self.sittings.all()

    def total_courses(self):
        return self.student.courses.all()

    def courses_created(self):
        return self.courses.all()


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=255, help_text="Your full name")
    image = models.ImageField(
        default='profile_default.jpg', upload_to='profile_pics')
    slug = models.SlugField(max_length=30, unique=True)
    about = models.TextField(default="A brief description about me")
    joined = models.DateTimeField("Date Joined", auto_now_add=True)
    wallet_address = models.CharField(
        max_length=35, help_text="Please ensure you submit waves address generated using AMADI wallet")
    telegram_id = models.CharField(max_length=100, null=True, blank=True, default="username",
                                   help_text="please input your correct telegram username to connect with friends, fellow quiz takers, and quiz masters")

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return reverse('piquest-auth:public_profile', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('piquest-auth:profile_update')

    def get_telegram_url(self):
        return f'{"t.me/"}{self.telegram_id}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.get_username())
        super().save(*args, **kwargs)


class Payment(models.Model):
    transaction_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
