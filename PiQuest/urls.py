from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

admin.site.site_header = 'PiQuest Admin'
admin.site.site_title = 'PiQuest Site Admin'

urlpatterns = [
    path('', include('user.urls', namespace='piquest-auth')),
    path('', include('main.urls', namespace='main')),
    path('project/', include('projects.urls', namespace='project')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('quiz/', include('quiz.urls', namespace='quiz')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("badges/", include("pinax.badges.urls", namespace="pinax_badges")),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
