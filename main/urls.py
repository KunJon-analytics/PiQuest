from django.urls import path
from .views import HomePageView, PrivacyPageView, pi_validation
from quiz.views import (CategoryDetail, CategoriesListView, CategoryCreate,
                        CategoryUpdate, CategoryDelete)

app_name = 'main'

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('validation-key.txt', pi_validation, name='pi_validation'),
    path('privacy/', PrivacyPageView.as_view(), name='privacy_page'),
    path('category/', CategoriesListView.as_view(), name='category_list'),
    path('category/create/', CategoryCreate.as_view(), name='category_create'),
    path('category/<slug>/update/',
         CategoryUpdate.as_view(), name='category_update'),
    path('category/<slug>/delete/',
         CategoryDelete.as_view(), name='category_delete'),
    path('category/<slug>/', CategoryDetail.as_view(), name='category_detail'),
]
