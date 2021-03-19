from django.urls import path, include
from django.conf.urls import url
from .views import project_detail, ProjectList, ArticleLinkCreate, ProjectCreate

app_name = 'project'

urlpatterns = [
    url(r'^$', ProjectList.as_view(), name='project_list'),
    url(r'^article/create/$', ArticleLinkCreate.as_view(), name='article_create'),
    url(r'^create/$', ProjectCreate.as_view(), name='project_create'),
    url(r'(?P<url>[\w\-]+)/$', project_detail, name='project_detail'),
]
