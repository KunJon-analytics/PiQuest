from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.db import transaction
from classroom.decorators import teacher_required
from quiz.models import Quiz, Category
from .forms import MCQAddForm, BaseAnswerInlineFormSet
from .models import MCQuestion, Answer


@login_required
@teacher_required
def add_multichoice(request, slug):
    quiz = get_object_or_404(Quiz, url=slug)
    category = get_object_or_404(Category, id=quiz.category.id)

    if request.method == 'POST':
        form = MCQAddForm(request.POST)
        if form.is_valid():
            figure = form.cleaned_data.get('figure')
            content = form.cleaned_data.get('content')
            explanation = form.cleaned_data.get('explanation')
            answer_order = form.cleaned_data.get('answer_order')
            question = MCQuestion.objects.create(
                figure=figure, content=content, explanation=explanation, answer_order=answer_order)
            question.category = category
            question.save()
            question.quiz.add(quiz)

            messages.success(
                request, 'You may now add answers/options to the question.')
            return redirect('quiz:multichoice_change', quiz.url, question.pk)
    else:
        form = MCQAddForm()

    context = {
        'title': 'Add multichoice question',
        'quiz': quiz,
        'form': form
    }
    return render(request, 'multichoice/multichoice_add_form.html', context)


@login_required
@teacher_required
def edit_multichoice(request, slug, question_pk):
    quiz = get_object_or_404(Quiz, url=slug, master=request.user)
    question = get_object_or_404(MCQuestion, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        MCQuestion,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('content', 'correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = MCQAddForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()

            messages.success(
                request, 'Multichoice question and answers are successfully saved!')
            return redirect('quiz:quiz_update', quiz.url)
    else:
        form = MCQAddForm(instance=question)
        formset = AnswerFormSet(instance=question)

    context = {
        'title': 'Edit Multichoice Question',
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    }

    return render(request, 'multichoice/multichoice_change_form.html', context)


@login_required
@teacher_required
def delete_multichoice(request, slug, question_pk):
    teacher = request.user
    quiz_get = get_object_or_404(Quiz, url=slug)
    question_get = get_object_or_404(MCQuestion, pk=question_pk)
    context = {}
    quiz = Quiz.objects.get(id=quiz_get.pk, master=teacher)
    context['title'] = "Delete multichoice question"
    context['quiz'] = quiz
    context['question'] = question_get

    if request.method == "POST":
        # delete object
        MCQuestion.objects.get(id=question_get.pk, quiz=quiz).delete()
        messages.success(
            request, 'The question has been successfully deleted.')
        # after deleting redirect to
        # home page
        return redirect('quiz:quiz_update', quiz.url)

    return render(request, "multichoice/multichoice_confirm_delete.html", context)
