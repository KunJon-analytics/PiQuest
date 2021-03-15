from django.contrib import admin

# Register your models here.
from .models import User, Creator, Taker


admin.site.register(User)
admin.site.register(Creator)
admin.site.register(Taker)