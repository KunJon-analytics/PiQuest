from django.urls import path

from essay.views import add_essay, edit_essay, delete_essay

from multichoice.views import add_multichoice, edit_multichoice, delete_multichoice

from true_false.views import add_true_false, edit_true_false, delete_true_false

from .views import QuizListView, ViewQuizListByCategory, QuizCreateView, \
    QuizUserProgressView, QuizMarkingList, QuizDelete, publish_quiz, \
    QuizMarkingDetail, QuizDetailView, QuizTake, edit_quiz, TriviaListView

app_name = 'quiz'

urlpatterns = [

    path('', view=QuizListView.as_view(), name='quiz_index'),

    path('master/', view=TriviaListView.as_view(), name='master_trivia_list'),

    path('category/<slug:category_name>/',
         view=ViewQuizListByCategory.as_view(), name='quiz_category_list_matching'),

    path('progress/', view=QuizUserProgressView.as_view(), name='quiz_progress'),

    path('marking/', view=QuizMarkingList.as_view(), name='quiz_marking'),

    path('marking/<int:pk>/', view=QuizMarkingDetail.as_view(),
         name='quiz_marking_detail'),

    path('create-quiz/', QuizCreateView.as_view(), name='quiz_create'),


    #  passes variable 'quiz_name' to quiz_take view
    path('<slug>/', view=QuizDetailView.as_view(), name='quiz_start_page'),

    path('<slug>/update/', view=edit_quiz, name='quiz_update'),

    path('<slug>/delete/', view=QuizDelete.as_view(), name='quiz_delete'),

    path('<slug>/publish/', view=publish_quiz, name='publish_quiz'),

    path('essay/<slug>/question/add/',
         add_essay, name='essay_add'),

    path('essay/<slug>/question/<int:question_pk>/',
         edit_essay, name='essay_change'),

    path('essay/<slug>/question/<int:question_pk>/delete/',
         delete_essay, name='essay_delete'),

    path('mcq/<slug>/question/add/',
         add_multichoice, name='multichoice_add'),

    path('mcq/<slug>/question/<int:question_pk>/',
         edit_multichoice, name='multichoice_change'),

    path('mcq/<slug>/question/<int:question_pk>/delete/',
         delete_multichoice, name='multichoice_delete'),

    path('true-false/<slug>/question/add/',
         add_true_false, name='true_false_add'),

    path('true-false/<slug>/question/<int:question_pk>/',
         edit_true_false, name='true_false_change'),

    path('true-false/<slug>/question/<int:question_pk>/delete/',
         delete_true_false, name='true_false_delete'),

    path('<slug:quiz_name>/take/', view=QuizTake.as_view(), name='quiz_question'),
]
