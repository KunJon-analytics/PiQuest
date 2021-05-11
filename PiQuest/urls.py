from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView, TemplateView
from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap
from puput import urls as puput_urls

admin.site.site_header = 'PiQuests Admin'
admin.site.site_title = 'PiQuests Site Admin'

urlpatterns = [
    path('', include('user.urls', namespace='piquest-auth')),
    path('', include('main.urls', namespace='main')),
    path('project/', include('projects.urls', namespace='project')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('quiz/', include('quiz.urls', namespace='quiz')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("badges/", include("pinax.badges.urls", namespace="pinax_badges")),
    path(
        route='blog_admin/',
        view=include(wagtailadmin_urls)
    ),
    path(
        route='documents/',
        view=include(wagtaildocs_urls)
    ),
    re_path(r'', include(puput_urls)),
    re_path(
        route='',
        view=include(wagtail_urls)
    ),
    path(
        route='sitemap.xml',
        view=sitemap
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
