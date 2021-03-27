from django.urls import path

from .views import QuizListView, ViewQuizListByCategory, QuizCreateView, QuestionUpdate, \
    QuizUserProgressView, QuizMarkingList, QuestionListView, QuestionCreateView, QuizDelete, \
    QuizMarkingDetail, QuizDetailView, QuizTake, QuestionDetailView, QuizUpdate, QuestionDelete

app_name = 'quiz'

urlpatterns = [

    path('', view=QuizListView.as_view(), name='quiz_index'),

    path('question/', view=QuestionListView.as_view(), name='question_index'),

    path('question/<int:pk>/', view=QuestionDetailView.as_view(), name='question_detail_page'),

    path('question/<int:pk>/update/', view=QuestionUpdate.as_view(), name='question_update'),


    path('question/<int:pk>/delete/', view=QuestionDelete.as_view(), name='question_delete'),

    path('category/<slug:category_name>/', view=ViewQuizListByCategory.as_view(), name='quiz_category_list_matching'),

    path('progress/', view=QuizUserProgressView.as_view(), name='quiz_progress'),

    path('marking/', view=QuizMarkingList.as_view(), name='quiz_marking'),

    path('marking/<int:pk>/', view=QuizMarkingDetail.as_view(), name='quiz_marking_detail'),

    path('create-quiz/', QuizCreateView.as_view(), name='quiz_create'),

    path('question/create/', QuestionCreateView.as_view(), name='question_create'),


    #  passes variable 'quiz_name' to quiz_take view
    path('<slug>/', view=QuizDetailView.as_view(), name='quiz_start_page'),

    path('<slug>/update/', view=QuizUpdate.as_view(), name='quiz_update'),

    path('<slug>/delete/', view=QuizDelete.as_view(), name='quiz_delete'),

    path('<slug:quiz_name>/take/', view=QuizTake.as_view(), name='quiz_question'),
]
