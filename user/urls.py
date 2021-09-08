from django.conf.urls import include
from django.urls import reverse_lazy, path
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import RedirectView, TemplateView

from .views import (ActivateAccount, DisableAccount, ProfileDetail, ToggleManager,
                    PublicProfileDetail, ProfileUpdate, ToggleTeacher, CampusAmbassadorsiew)


app_name = 'piquest-auth'

urlpatterns = [
    path('user/', RedirectView.as_view(pattern_name='piquest-auth:login', permanent=False)),
    path('accounts/', RedirectView.as_view(pattern_name=('piquest-auth:profile'), permanent=False)),
    path('disable/', DisableAccount.as_view(), name='disable'),
    path('profile/', ProfileDetail.as_view(), name='profile'),
    path('toggle-master/', ToggleTeacher.as_view(), name='toggle_teacher'),
    path('toggle-manager/', ToggleManager.as_view(), name='toggle_manager'),
    path('profile/edit/', ProfileUpdate.as_view(), name='profile_update'),
    path('profile/<slug>/', PublicProfileDetail.as_view(), name='public_profile'),
    path('campus-ambassador/', CampusAmbassadorsiew.as_view(), name='campus_ambassador'),
]
