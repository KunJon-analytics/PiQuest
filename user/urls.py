from django.conf.urls import include
from django.urls import reverse_lazy, path
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import RedirectView, TemplateView

from .views import (ActivateAccount, CreateAccount, DisableAccount, ProfileDetail, 
PublicProfileDetail, ResendActivationEmail,  ProfileUpdate)


app_name = 'piquest-auth'

urlpatterns = [
    path('user/',RedirectView.as_view(pattern_name='piquest-auth:login', permanent=False)),
    path('activate/<slug:uidb64>/<slug:token>/',ActivateAccount.as_view(),name='activate'),
    path('activate', RedirectView.as_view(pattern_name=('piquest-auth:resend_activation'), permanent=False)),
    path('activate/resend/', ResendActivationEmail.as_view(), name='resend_activation'),
    path('create/', CreateAccount.as_view(), name='create'),
    path('create/done/',TemplateView.as_view(template_name=('user/user_create_done.html')),name='create_done'),
    path('disable/', DisableAccount.as_view(), name='disable'),
    path('login/', auth_views.LoginView.as_view(template_name = 'user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'user/logged_out.html', extra_context = {'form': AuthenticationForm}) , name='logout'),
    path('profile/', ProfileDetail.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdate.as_view(), name='profile_update'),
    path('profile/<slug>/', PublicProfileDetail.as_view(), name='public_profile'),
]
