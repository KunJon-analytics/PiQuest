from django.urls import path, include
from django.conf.urls import url
from .views import project_detail, ProjectList

app_name = 'project'

urlpatterns = [
    url(r'^$', ProjectList.as_view(), name='project_list'),
    url(r'(?P<url>[\w\-]+)/$', project_detail, name='project_detail'),
]
