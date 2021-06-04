from django.contrib import admin
from .models import Profile, User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')  # whatever
    list_filter = ('is_master',)
    search_fields = ('username',)

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
