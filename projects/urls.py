from django.urls import path, include
from django.conf.urls import url
from .views import (ProjectDetail, ProjectList, ArticleLinkCreate, ArticleDelete,
ProjectCreate, ArticleUpdate, ProjectUpdate, ProjectDelete)

app_name = 'project'

urlpatterns = [
    path('', ProjectList.as_view(), name='project_list'),
    path('<slug:project_slug>/add_article_link/', ArticleLinkCreate.as_view(), name='articlelink_create'),
    path('<slug:project_slug>/<slug:articlelink_slug>/update/', ArticleUpdate.as_view(), name='articlelink_update'),
    path('<slug:project_slug>/<slug:articlelink_slug>/delete/', ArticleDelete.as_view(), name='articlelink_delete'),
    path('create/', ProjectCreate.as_view(), name='project_create'),
    path('<slug>/update/', ProjectUpdate.as_view(), name='project_update'),
    path('<slug>/delete/', ProjectDelete.as_view(), name='project_delete'),
    path('<slug>/', ProjectDetail.as_view(), name='project_detail'),
]
