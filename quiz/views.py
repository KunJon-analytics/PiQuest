import random
from time import sleep
from django.contrib.messages.api import error

import pywaves as pw

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from user.decorators import staff_required, master_required
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView, TemplateView, FormView

from main.utils import PageLinksMixin, PostFormValidMixin
from main.bot import post_published_quiz_on_telegram, post_rewards_sent_on_telegram, post_new_winner_on_telegram
from .forms import QuestionForm, EssayForm, CategoryForm, QuizCUForm, TriviaEditForm
from .models import Quiz, Category, Progress, Sitting, Question, Winner
from essay.models import Essay_Question
from multichoice.models import MCQuestion
from true_false.models import TF_Question
from user.models import Payment, piquestsAddress, WART_ASSET

WVS = 10**8

class QuizMarkerMixin(object):
    @method_decorator(login_required)
    @method_decorator(permission_required('quiz.view_sittings', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkerMixin, self).dispatch(*args, **kwargs)


class SittingFilterTitleMixin(object):
    def get_queryset(self):
        queryset = super(SittingFilterTitleMixin, self).get_queryset()
        quiz_filter = self.request.GET.get('quiz_filter')
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)

        return queryset


class QuizListView(ListView):
    model = Quiz
    paginate_by = 8
    categories = Category.objects.all()

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        return queryset.filter(draft=False)

    def get_context_data(self, **kwargs):
        context = super(QuizListView, self)\
            .get_context_data(**kwargs)

        context['categories'] = self.categories
        context['title'] = 'Choose from our collection of quizzes'
        return context


@method_decorator([login_required, master_required], name='dispatch')
class TriviaListView(ListView):
    model = Quiz
    context_object_name = 'quizzes'
    extra_context = {
        'title': 'My Quizzes'
    }
    template_name = 'quiz/master_trivia_list.html'
    paginate_by = 10

    def get_queryset(self):
        """Gets the quizzes that the logged in teacher owns.
        Counts the questions and the number of students who took the quiz."""
        queryset = Quiz.objects.filter(master=self.request.user) \
            .annotate(questions_count=Count('question', distinct=True)) \
            .order_by('-id')
        return queryset


class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'url'

    def get_context_data(self, *args, **kwargs):
        context = super(QuizDetailView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        if self.object.exam_paper and self.object.single_attempt:
            pass_value = round(
                (self.object.pass_mark * self.object.max_questions) / 100)
            leaders = Sitting.objects.filter(complete=True, quiz__title=self.object.title,
                                             current_score__gte=pass_value).order_by('end')[:self.object.number_of_winners]
            context['leaderboard'] = leaders
        title = self.object.title
        context['title'] = title
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


@method_decorator([login_required, master_required], name='dispatch')
class QuizCreateView(PostFormValidMixin, CreateView):
    form_class = QuizCUForm
    template_name = 'quiz/quiz_create_form.html'
    model = Quiz

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "Create a new trivia"
        context['title'] = title
        return context


@login_required
@master_required
def edit_quiz(request, slug):
    quiz = get_object_or_404(Quiz, url=slug, master=request.user)
    essay_question = Essay_Question.objects.filter(quiz=quiz)
    multichoice_questions = MCQuestion.objects.filter(quiz=quiz)
    tf_questions = TF_Question.objects.filter(quiz=quiz)
    publish_ready = quiz.publish_ready()
    payment_ready = quiz.winners_payment_ready()
    payment = quiz.get_total_payment()

    if request.method == 'POST':
        form = TriviaEditForm(data=request.POST, instance=quiz)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()

            messages.success(request, 'The quiz was successfully changed.')
            return redirect('quiz:quiz_update', quiz.url)
    else:
        form = TriviaEditForm(instance=quiz)

    context = {
        'title': 'Edit Quiz',
        'quiz': quiz,
        'essay_questions': essay_question,
        'multichoice_questions': multichoice_questions,
        'tf_questions': tf_questions,
        'form': form,
        'publish_ready': publish_ready,
        'payment_ready': payment_ready,
        'payment': payment
    }
    return render(request, 'quiz/quiz_update_form.html', context)


@login_required
@master_required
@csrf_protect
def pay_quiz_winners(request, slug):
    winners = Winner.objects.filter(quiz__url=slug, paid=False)
    quiz = get_object_or_404(Quiz, url=slug, master=request.user)
    number_of_winners = quiz.number_of_winners
    payment = quiz.get_total_payment()
    attachment = 'Payment for {quiz} trivia winners on PiQuests'.format(quiz=str(quiz.title))

    if winners.count() == number_of_winners:
        transfers = list(winners.values('recipient', 'amount'))
        for d in transfers:
            float_amount = float(d['amount'])
            d['amount'] = int(float_amount*WVS)
        tx = piquestsAddress.massTransferAssets(transfers, WART_ASSET, attachment=attachment)
        sleep(5.0)
        if "error" not in pw.tx(tx["id"]):
            winners.update(paid=True)
            quiz.single_attempt = False
            quiz.exam_paper = False
            quiz.save()
            user = get_user(request)
            amount = quiz.get_total_payment()
            payment = Payment()
            payment.transaction_id = tx["id"]
            payment.user = user
            payment.amount = amount
            payment.save()
            post_rewards_sent_on_telegram(payment=payment, quiz=quiz)
            messages.success(
                request, '{amount} WART have been sent to {number_of_winners} winners. Transaction ID: {txid}'.format(amount=amount, number_of_winners=number_of_winners, txid=tx["id"]))
        else:
            messages.error(
                request, '{error}'.format(error=pw.tx(tx["id"])))     
    return redirect('quiz:quiz_update', quiz.url)


@login_required
@master_required
@csrf_protect
def publish_quiz(request, slug):
    quiz = get_object_or_404(Quiz, url=slug, master=request.user)
    publish_ready = quiz.publish_ready()
    payment = quiz.get_total_payment()

    if request.is_ajax():
        quiz.draft = False
        quiz.save()
        user = get_user(request)
        amount = quiz.get_total_payment()
        payment = Payment()
        payment.transaction_id = get_random_string(length=32)
        payment.user = user
        payment.amount = amount
        payment.save()
        data = {
            'url': reverse_lazy('quiz:quiz_update', kwargs={'slug': quiz.url}),
        }
        post_published_quiz_on_telegram(quiz=quiz)
        messages.success(
            request, 'The quiz will be published in some minutes.')
        return JsonResponse({'data': data})

    context = {
        'title': 'Publish Quiz',
        'quiz': quiz,
        'publish_ready': publish_ready,
        'payment': payment
    }
    return render(request, 'quiz/quiz_publish_form.html', context)


@method_decorator([login_required, master_required], name='dispatch')
class QuizDelete(UserPassesTestMixin, DeleteView):

    model = Quiz
    slug_field = 'url'
    success_url = reverse_lazy('quiz:quiz_index')
    template_name = 'quiz/quiz_confirm_delete.html'

    def test_func(self):
        quiz = self.get_object()
        if self.request.user == quiz.master:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "Delete Trivia"
        context['title'] = title
        return context


class CategoryDetail(DetailView):
    model = Category
    template_name = 'quiz/category_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['title'] = self.get_object()
        return super().get_context_data(**kwargs)


class CategoriesListView(PageLinksMixin, ListView):
    model = Category
    page_kwarg = 'page'
    paginate_by = 16  # 16 items per page
    template_name = 'quiz/category_list.html'

    def get_context_data(self, **kwargs):
        context = super(CategoriesListView, self)\
            .get_context_data(**kwargs)

        context['title'] = 'See our collection of interests'
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class CategoryCreate(CreateView):
    form_class = CategoryForm
    template_name = 'main/category_create_form.html'


@method_decorator([login_required, staff_required], name='dispatch')
class CategoryUpdate(UpdateView):
    form_class = CategoryForm
    model = Category
    template_name = 'main/category_update_form.html'


@method_decorator([login_required, staff_required], name='dispatch')
class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('main:category_list')
    template_name = 'main/category_confirm_delete.html'


class ViewQuizListByCategory(ListView):
    model = Quiz
    template_name = 'view_quiz_category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            category=self.kwargs['category_name']
        )

        return super(ViewQuizListByCategory, self).\
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListByCategory, self)\
            .get_context_data(**kwargs)

        context['category'] = self.category
        return context

    def get_queryset(self):
        queryset = super(ViewQuizListByCategory, self).get_queryset()
        return queryset.filter(category=self.category, draft=False)


class QuizUserProgressView(TemplateView):
    template_name = 'progress.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuizUserProgressView, self)\
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuizUserProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        context['cat_scores'] = progress.list_all_cat_scores
        context['exams'] = progress.show_exams()
        return context


class QuizMarkingList(QuizMarkerMixin, SittingFilterTitleMixin, ListView):
    model = Sitting

    def get_queryset(self):
        user = self.request.user
        queryset = super(QuizMarkingList, self).get_queryset()\
                                               .filter(complete=True, quiz__master=user)

        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(
                user__profile__name__icontains=user_filter)

        return queryset


class QuizMarkingDetail(QuizMarkerMixin, DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get('qid', None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            if int(q_to_toggle) in sitting.get_incorrect_questions:
                sitting.remove_incorrect_question(q)
            else:
                sitting.add_incorrect_question(q)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(QuizMarkingDetail, self).get_context_data(**kwargs)
        context['questions'] =\
            context['sitting'].get_questions(with_answers=True)
        return context


class QuizTake(FormView):
    form_class = QuestionForm
    template_name = 'question.html'
    result_template_name = 'result.html'
    single_complete_template_name = 'single_complete.html'
    no_wart_template_name = 'no_wart.html'
    wrong_public_key_template_name = 'wrong_public_key.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['quiz_name'])
        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        try:
            self.logged_in_user = self.request.user.is_authenticated()
        except TypeError:
            self.logged_in_user = self.request.user.is_authenticated

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(request.user,
                                                        self.quiz)
        else:
            self.sitting = self.anon_load_sitting()

        if self.sitting is False:
            return render(request, self.single_complete_template_name)

        if self.quiz.single_attempt:
            balance = request.user.get_wallet_balance() 
            if balance < 0:
                return render(request, self.wrong_public_key_template_name)
            if balance < 10:
                return render(request, self.no_wart_template_name)


        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        if self.logged_in_user:
            self.question = self.sitting.get_first_question()
            self.progress = self.sitting.progress()
        else:
            self.question = self.anon_next_question()
            self.progress = self.anon_sitting_progress()

        if self.question.__class__ is Essay_Question:
            form_class = EssayForm
        else:
            form_class = self.form_class

        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        if self.logged_in_user:
            self.form_valid_user(form)
            if self.sitting.get_first_question() is False:
                return self.final_result_user()
        else:
            self.form_valid_anon(form)
            if not self.request.session[self.quiz.anon_q_list()]:
                return self.final_result_anon()

        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz'] = self.quiz
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        return context

    def form_valid_user(self, form):
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.sitting.add_to_score(1)
            progress.update_score(self.question, 1, 1)
        else:
            self.sitting.add_incorrect_question(self.question)
            progress.update_score(self.question, 0, 1)

        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                               .__class__.__name__: True}}
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        results = {
            'quiz': self.quiz,
            'score': self.sitting.get_current_score,
            'max_score': self.sitting.get_max_score,
            'percent': self.sitting.get_percent_correct,
            'sitting': self.sitting,
            'previous': self.previous,
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results['questions'] =\
                self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] =\
                self.sitting.get_incorrect_questions

        if self.quiz.exam_paper is False:
            self.sitting.delete()

        return render(self.request, self.result_template_name, results)

    def anon_load_sitting(self):
        if self.quiz.single_attempt is True:
            return False

        if self.quiz.anon_q_list() in self.request.session:
            return self.request.session[self.quiz.anon_q_list()]
        else:
            return self.new_anon_quiz_session()

    def new_anon_quiz_session(self):
        """
        Sets the session variables when starting a quiz for the first time
        as a non signed-in user
        """
        self.request.session.set_expiry(259200)  # expires after 3 days
        questions = self.quiz.get_questions()
        question_list = [question.id for question in questions]

        if self.quiz.random_order is True:
            random.shuffle(question_list)

        if self.quiz.max_questions and (self.quiz.max_questions
                                        < len(question_list)):
            question_list = question_list[:self.quiz.max_questions]

        # session score for anon users
        self.request.session[self.quiz.anon_score_id()] = 0

        # session list of questions
        self.request.session[self.quiz.anon_q_list()] = question_list

        # session list of question order and incorrect questions
        self.request.session[self.quiz.anon_q_data()] = dict(
            incorrect_questions=[],
            order=question_list,
        )

        return self.request.session[self.quiz.anon_q_list()]

    def anon_next_question(self):
        next_question_id = self.request.session[self.quiz.anon_q_list()][0]
        return Question.objects.get_subclass(id=next_question_id)

    def anon_sitting_progress(self):
        total = len(self.request.session[self.quiz.anon_q_data()]['order'])
        answered = total - len(self.request.session[self.quiz.anon_q_list()])
        return (answered, total)

    def form_valid_anon(self, form):
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct:
            self.request.session[self.quiz.anon_score_id()] += 1
            anon_session_score(self.request.session, 1, 1)
        else:
            anon_session_score(self.request.session, 0, 1)
            self.request\
                .session[self.quiz.anon_q_data()]['incorrect_questions']\
                .append(self.question.id)

        self.previous = {}
        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                               .__class__.__name__: True}}

        self.request.session[self.quiz.anon_q_list()] =\
            self.request.session[self.quiz.anon_q_list()][1:]

    def final_result_anon(self):
        score = self.request.session[self.quiz.anon_score_id()]
        q_order = self.request.session[self.quiz.anon_q_data()]['order']
        max_score = len(q_order)
        percent = int(round((float(score) / max_score) * 100))
        session, session_possible = anon_session_score(self.request.session)
        if score == 0:
            score = "0"

        results = {
            'score': score,
            'max_score': max_score,
            'percent': percent,
            'session': session,
            'possible': session_possible
        }

        del self.request.session[self.quiz.anon_q_list()]

        if self.quiz.answers_at_end:
            results['questions'] = sorted(
                self.quiz.question_set.filter(id__in=q_order)
                                      .select_subclasses(),
                key=lambda q: q_order.index(q.id))

            results['incorrect_questions'] = (
                self.request
                    .session[self.quiz.anon_q_data()]['incorrect_questions'])

        else:
            results['previous'] = self.previous

        del self.request.session[self.quiz.anon_q_data()]

        return render(self.request, 'result.html', results)


def anon_session_score(session, to_add=0, possible=0): 
    """
    Returns the session score for non-signed in users.
    If number passed in then add this to the running total and
    return session score.

    examples:
        anon_session_score(1, 1) will add 1 out of a possible 1
        anon_session_score(0, 2) will add 0 out of a possible 2
        x, y = anon_session_score() will return the session score
                                    without modification

    Left this as an individual function for unit testing
    """
    if "session_score" not in session:
        session["session_score"], session["session_score_possible"] = 0, 0

    if possible > 0:
        session["session_score"] += to_add
        session["session_score_possible"] += possible

    return session["session_score"], session["session_score_possible"]


# @login_required
# @master_required
# @csrf_protect
# def get_old_quiz_winners(request, slug):
#     quiz = get_object_or_404(Quiz, url=slug, master=request.user)
#     pass_value = round(
#                 (quiz.pass_mark * quiz.max_questions) / 100)
#     leaders = Sitting.objects.filter(complete=True, quiz__title=quiz.title,
#                                              current_score__gte=pass_value).order_by('end')[:quiz.number_of_winners]
#     for sitting in leaders:
#         winner = Winner()
#         winner.quiz = sitting.quiz
#         winner.user = sitting.user
#         winner.save()
#         post_new_winner_on_telegram(winner=winner)
#         sleep(0.1)
#     messages.success(
#             request, '{number_of_winners} winners have being added to the winners list for winning {quiz}.'.format(number_of_winners=quiz.number_of_winners, quiz=quiz.title))     
#     return redirect('quiz:quiz_update', quiz.url)