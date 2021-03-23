try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from .views import QuizListView, ViewQuizListByCategory, QuizCreateView, QuestionUpdate, \
    QuizUserProgressView, QuizMarkingList, QuestionListView, QuestionCreateView, QuizDelete, \
    QuizMarkingDetail, QuizDetailView, QuizTake, QuestionDetailView, QuizUpdate, QuestionDelete

app_name = 'quiz'

urlpatterns = [

    url(r'^$',
        view=QuizListView.as_view(),
        name='quiz_index'),

    url(r'^question/$',
        view=QuestionListView.as_view(),
        name='question_index'),

    url(r'^question/(?P<pk>[\d.]+)/$',
        view=QuestionDetailView.as_view(),
        name='question_detail_page'),

    url(r'^question/(?P<pk>[\d.]+)/update/$',
        view=QuestionUpdate.as_view(),
        name='question_update'),


    url(r'^question/(?P<pk>[\d.]+)/delete/$',
        view=QuestionDelete.as_view(),
        name='question_delete'),

    url(r'^category/(?P<category_name>[\w|\W-]+)/$',
        view=ViewQuizListByCategory.as_view(),
        name='quiz_category_list_matching'),

    url(r'^progress/$',
        view=QuizUserProgressView.as_view(),
        name='quiz_progress'),

    url(r'^marking/$',
        view=QuizMarkingList.as_view(),
        name='quiz_marking'),

    url(r'^marking/(?P<pk>[\d.]+)/$',
        view=QuizMarkingDetail.as_view(),
        name='quiz_marking_detail'),

    url(r'^create/$', QuizCreateView.as_view(), name='quiz_create'),

    url(r'^question/create/$', QuestionCreateView.as_view(), name='question_create'),


    #  passes variable 'quiz_name' to quiz_take view
    url(r'^(?P<slug>[\w-]+)/$', view=QuizDetailView.as_view(), name='quiz_start_page'),

    url(r'^(?P<slug>[\w-]+)/update/$', view=QuizUpdate.as_view(), name='quiz_update'),

    url(r'^(?P<slug>[\w-]+)/delete/$', view=QuizDelete.as_view(), name='quiz_delete'),

    url(r'^(?P<quiz_name>[\w-]+)/take/$',
        view=QuizTake.as_view(),
        name='quiz_question'),
]
