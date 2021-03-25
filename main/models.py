# from django.db import models
# from django.contrib.auth.models import AbstractUser


# # Create your models here.
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
