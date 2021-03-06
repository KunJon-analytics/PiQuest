from django import forms
from django.forms.widgets import RadioSelect, Textarea
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user
from django.contrib import messages
from .models import Category, Quiz
from projects.forms import CleanUrlMixin


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=RadioSelect)


class EssayForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(EssayForm, self).__init__(*args, **kwargs)
        self.fields["answers"] = forms.CharField(
            widget=Textarea(attrs={'style': 'width:100%'}))


class CategoryForm(CleanUrlMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def clean_category(self):
        return self.cleaned_data['category'].lower()


# quizform should validate against create, progress, marking
class QuizCUForm(CleanUrlMixin, forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ('master', 'url', 'draft', 'single_attempt', 'exam_paper')

    def clean_url(self):
        new_slug = (self.cleaned_data['url'].lower())
        if new_slug == ['create', 'progress', 'marking', 'category', 'question']:
            raise ValidationError('You are not allowed to use this URL.')
        return new_slug

    def save(self, request, commit=True):
        quiz = super().save(commit=False)
        if not quiz.pk:
            quiz.master = get_user(request)
            quiz.draft = True
            quiz.single_attempt = True
        if commit:
            quiz.save()
            self.save_m2m()
            messages.add_message(
                request, messages.SUCCESS, 'Quiz created successfully, you can add questions by editing the quiz.')
        return quiz


class TriviaEditForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description', 'image', 'success_text', 'fail_text')
