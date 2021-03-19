from django.urls import path, include
from django.conf.urls import url
from .views import HomePageView
from quiz.views import category_detail, CategoriesListView, CategoryCreate

app_name = 'main'

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    url(r'^category/$', CategoriesListView.as_view(), name='category_list'),
    url(r'^category/create/$', CategoryCreate.as_view(), name='category_create'),
    url(r'^category/(?P<url>[\w\-]+)/$', category_detail, name='category_detail'),
]
