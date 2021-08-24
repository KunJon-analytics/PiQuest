from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from classroom.decorators import teacher_required
from quiz.models import Quiz, Category
from .forms import TFAddForm
from .models import TF_Question


@login_required
@teacher_required
def add_true_false(request, slug):
    quiz = get_object_or_404(Quiz, url=slug)
    category = get_object_or_404(Category, id=quiz.category.id)

    if request.method == 'POST':
        form = TFAddForm(request.POST)
        if form.is_valid():
            figure = form.cleaned_data.get('figure')
            content = form.cleaned_data.get('content')
            explanation = form.cleaned_data.get('explanation')
            correct = form.cleaned_data.get('correct')
            question = TF_Question.objects.create(
                figure=figure, content=content, explanation=explanation, correct=correct)
            question.category = category
            question.save()
            question.quiz.add(quiz)

            messages.success(
                request, 'You can still edit the question.')
            return redirect('quiz:true_false_change', quiz.url, question.pk)
    else:
        form = TFAddForm()

    context = {
        'title': 'Add True / False question',
        'quiz': quiz,
        'form': form
    }
    return render(request, 'true_false/true_false_add_form.html', context)


@login_required
@teacher_required
def edit_true_false(request, slug, question_pk):
    quiz = get_object_or_404(Quiz, url=slug, master=request.user)
    question = get_object_or_404(TF_Question, pk=question_pk, quiz=quiz)

    if request.method == 'POST':
        form = TFAddForm(request.POST, instance=question)
        if form.is_valid():
            form.save()

            messages.success(
                request, 'true/false question saved succesfully!')
            return redirect('quiz:quiz_update', quiz.url)
    else:
        form = TFAddForm(instance=question)

    context = {
        'title': 'Edit true/false Question',
        'quiz': quiz,
        'question': question,
        'form': form
    }

    return render(request, 'true_false/true_false_change_form.html', context)


@login_required
@teacher_required
def delete_true_false(request, slug, question_pk):
    teacher = request.user
    quiz_get = get_object_or_404(Quiz, url=slug)
    question_get = get_object_or_404(TF_Question, pk=question_pk)
    context = {}
    quiz = Quiz.objects.get(id=quiz_get.pk, master=teacher)
    context['title'] = "Delete true/false question"
    context['quiz'] = quiz
    context['question'] = question_get

    if request.method == "POST":
        # delete object
        TF_Question.objects.get(id=question_get.pk, quiz=quiz).delete()
        messages.success(
            request, 'The question has been successfully deleted.')
        # after deleting redirect to
        # home page
        return redirect('quiz:quiz_update', quiz.url)

    return render(request, "true_false/true_false_confirm_delete.html", context)
