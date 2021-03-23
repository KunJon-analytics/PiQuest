from django.urls import path, include
from django.conf.urls import url
from .views import HomePageView
from quiz.views import (CategoryDetail, CategoriesListView, CategoryCreate, 
CategoryUpdate, CategoryDelete

)

app_name = 'main'

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    url(r'^category/$', CategoriesListView.as_view(), name='category_list'),
    url(r'^category/create/$', CategoryCreate.as_view(), name='category_create'),
    url(r'^category/(?P<slug>[\w\-]+)/update/$', CategoryUpdate.as_view(), name='category_update'),
    url(r'^category/(?P<slug>[\w\-]+)/delete/$', CategoryDelete.as_view(), name='category_delete'),
    url(r'^category/(?P<slug>[\w\-]+)/$', CategoryDetail.as_view(), name='category_detail'),
]

