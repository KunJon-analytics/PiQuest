# from django.contrib.auth.models import AbstractUser
from django.db import models
from pinax.badges.base import Badge, BadgeAwarded
from pinax.badges.registry import badges
import quiz.models as qm


# Create your models here.
class WinnerBadge(Badge):
    slug = "winnings"
    levels = ["Winner",]
    events = [
        "mark_quiz_complete",
    ]
    multiple = True

    def award(self, **state):
        user = state["user"]
        if_passed = qm.Sitting.objects.get(user=user).check_if_passed
        if_complete = qm.Sitting.objects.get(user=user).complete
        if(if_passed and if_complete):
            return BadgeAwarded()

badges.register(WinnerBadge)




# class User(AbstractUser):
#     pass


# class Creator(models.Model):

#     PUBLIC_CHAIN_CHOICES = (
#         ('Ethereum', 'Ethereum'),
#         ('Binance Smart Chain', 'Binance Smart Chain'),
#         ('Neo', 'Neo'),
#         ('Waves', 'Waves'),
#         ('Pi Network', 'PiNetwork'),
#     )

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     wallet_address = models.CharField(max_length=50)
#     telegram_id = models.CharField(max_length=50)
#     twitter_id = models.CharField(max_length=50)
#     public_chain = models.CharField(choices=PUBLIC_CHAIN_CHOICES ,max_length=50)

#     def __str__(self):
#         return self.telegram_id



# class Taker(models.Model):

#     PUBLIC_CHAIN_CHOICES = (
#         ('Ethereum', 'Ethereum'),
#         ('Binance Smart Chain', 'Binance Smart Chain'),
#         ('Neo', 'Neo'),
#         ('Waves', 'Waves'),
#         ('Pi Network', 'PiNetwork'),
#     )

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     wallet_address = models.CharField(max_length=50)
#     telegram_id = models.CharField(max_length=50)
#     twitter_id = models.CharField(max_length=50)
#     public_chain = models.CharField(choices=PUBLIC_CHAIN_CHOICES ,max_length=50)

#     def __str__(self):
#         return f"{self.user.first_name} {self.user.last_name}"
