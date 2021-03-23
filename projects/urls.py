from django.urls import path, include
from django.conf.urls import url
from .views import (ProjectDetail, ProjectList, ArticleLinkCreate, ArticleDelete,
ProjectCreate, ArticleUpdate, ProjectUpdate, ProjectDelete
)

app_name = 'project'

urlpatterns = [
    url(r'^$', ProjectList.as_view(), name='project_list'),
    url(r'^(?P<project_slug>[\w\-]+)/'r'add_article_link/$', ArticleLinkCreate.as_view(), name='articlelink_create'),
    url(r'^(?P<project_slug>[\w\-]+)/'r'(?P<articlelink_slug>[\w\-]+)/'r'update/$', ArticleUpdate.as_view(), name='articlelink_update'),
    url(r'^(?P<project_slug>[\w\-]+)/'r'(?P<articlelink_slug>[\w\-]+)/'r'delete/$', ArticleDelete.as_view(), name='articlelink_delete'),
    url(r'^create/$', ProjectCreate.as_view(), name='project_create'),
    url(r'(?P<slug>[\w\-]+)/update/$', ProjectUpdate.as_view(), name='project_update'),
    url(r'(?P<slug>[\w\-]+)/delete/$', ProjectDelete.as_view(), name='project_delete'),
    url(r'(?P<slug>[\w\-]+)/$', ProjectDetail.as_view(), name='project_detail'),
]
