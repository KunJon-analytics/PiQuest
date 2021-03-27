import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.views import (
    LoginView, PasswordChangeDoneView,
    LogoutView, PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

admin.site.site_header = 'PiQuest Admin'
admin.site.site_title = 'PiQuest Site Admin'

urlpatterns = [
    path('', include('user.urls', namespace='piquest-auth')),
    path('', include('main.urls', namespace='main')),
    path('project/', include('projects.urls', namespace='project')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('quiz/', include('quiz.urls', namespace='quiz')),
    path('password/', RedirectView.as_view(pattern_name='reset-password', permanent=False)),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('change-password/', PasswordChangeView.as_view(), name='pw_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='pw_change_done'),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('accounts/', include('allauth.urls')),
]


    