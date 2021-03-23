from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('project/', include('projects.urls', namespace='project')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('quiz/', include('quiz.urls', namespace='quiz')),
]
