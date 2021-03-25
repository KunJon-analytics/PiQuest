try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from .views import QuizListView, ViewQuizListByCategory, QuizCreateView, QuestionUpdate, \
    QuizUserProgressView, QuizMarkingList, QuestionListView, QuestionCreateView, QuizDelete, \
    QuizMarkingDetail, QuizDetailView, QuizTake, QuestionDetailView, QuizUpdate, QuestionDelete

app_name = 'quiz'

urlpatterns = [

    url('', view=QuizListView.as_view(), name='quiz_index'),

    url('question/', view=QuestionListView.as_view(), name='question_index'),

    url('question/<int:pk>/', view=QuestionDetailView.as_view(), name='question_detail_page'),

    url('question/<int:pk>/update/', view=QuestionUpdate.as_view(), name='question_update'),


    url('question/<int:pk>/delete/', view=QuestionDelete.as_view(), name='question_delete'),

    url('category/<slug:category_name>/', view=ViewQuizListByCategory.as_view(), name='quiz_category_list_matching'),

    url('progress/', view=QuizUserProgressView.as_view(), name='quiz_progress'),

    url('marking/', view=QuizMarkingList.as_view(), name='quiz_marking'),

    url('marking/<int:pk>/', view=QuizMarkingDetail.as_view(), name='quiz_marking_detail'),

    url('create/', QuizCreateView.as_view(), name='quiz_create'),

    url('question/create/', QuestionCreateView.as_view(), name='question_create'),


    #  passes variable 'quiz_name' to quiz_take view
    url('<slug>/', view=QuizDetailView.as_view(), name='quiz_start_page'),

    url('<slug>/update/', view=QuizUpdate.as_view(), name='quiz_update'),

    url('<slug>/delete/', view=QuizDelete.as_view(), name='quiz_delete'),

    url('<slug:quiz_name>/take/', view=QuizTake.as_view(), name='quiz_question'),
]
