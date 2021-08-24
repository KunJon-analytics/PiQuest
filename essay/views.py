from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from classroom.decorators import teacher_required
from quiz.models import Quiz, Category
from .forms import EssayAddForm
from .models import Essay_Question


@login_required
@teacher_required
def add_essay(request, slug):
    quiz = get_object_or_404(Quiz, url=slug)
    category = get_object_or_404(Category, id=quiz.category.id)
    # TODO add sub_category to the field

    if request.method == 'POST':
        form = EssayAddForm(request.POST)
        if form.is_valid():
            figure = form.cleaned_data.get('figure')
            content = form.cleaned_data.get('content')
            explanation = form.cleaned_data.get('explanation')
            question = Essay_Question.objects.create(
                figure=figure, content=content, explanation=explanation)
            question.category = category
            question.save()
            question.quiz.add(quiz)

            messages.success(
                request, 'Nice job!!! you have added an essay question')
            messages.info(
                request, 'Please note that you will need to mark essay questions')
            return redirect('quiz:essay_change', quiz.url, question.pk)
    else:
        form = EssayAddForm()

    context = {
        'title': 'Add question',
        'quiz': quiz,
        'form': form
    }
    return render(request, 'essay/essay_add_form.html', context)


@login_required
@teacher_required
def edit_essay(request, slug, question_pk):
    quiz = get_object_or_404(Quiz, url=slug, master=request.user)
    question = get_object_or_404(Essay_Question, pk=question_pk, quiz=quiz)

    if request.method == 'POST':
        form = EssayAddForm(request.POST, instance=question)
        if form.is_valid():
            form.save()

            messages.success(
                request, 'You have updated the essay question')
            return redirect('quiz:quiz_update', quiz.url)
    else:
        form = EssayAddForm(instance=question)

    context = {
        'title': 'Edit Question',
        'quiz': quiz,
        'question': question,
        'form': form,
    }

    return render(request, 'essay/essay_change_form.html', context)


@login_required
@teacher_required
def delete_essay(request, slug, question_pk):
    teacher = request.user
    quiz_get = get_object_or_404(Quiz, url=slug)
    question_get = get_object_or_404(Essay_Question, pk=question_pk)
    context = {}
    quiz = Quiz.objects.get(id=quiz_get.pk, master=teacher)
    context['title'] = "Delete essay question"
    context['quiz'] = quiz
    context['question'] = question_get

    if request.method == "POST":
        # delete object
        Essay_Question.objects.get(id=question_get.pk, quiz=quiz).delete()
        messages.success(
            request, 'The essay question has been successfully deleted.')
        # after deleting redirect to
        # home page
        return redirect('quiz:quiz_update', quiz.url)

    return render(request, "essay/essay_confirm_delete.html", context)
