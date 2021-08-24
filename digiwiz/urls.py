"""digiwiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ckeditor_uploader import views as uploader_views
from classroom.views import classroom, students, teachers
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.decorators.cache import never_cache


urlpatterns = [
    path('', include('classroom.urls')),
    path('activate-student/<str:uidb64>/<str:token>',
         students.activate, name='activate_student'),
    path('activate-teacher/<str:uidb64>/<str:token>',
         teachers.activate, name='activate_teacher'),
    path('browse-courses/', classroom.browse_courses, name='browse_courses'),
    path('browse-courses/<int:subject_pk>/',
         classroom.browse_courses_subject, name='browse_courses_subject'),
    path('ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(uploader_views.browse),
         name='ckeditor_browse'),
    path('course/details/<int:pk>/',
         classroom.CourseDetailView.as_view(), name='course_details'),
    path('course/details/<int:pk>/lesson',
         students.LessonListView.as_view(), name='lesson_list'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
]
