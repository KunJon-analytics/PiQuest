from django import forms
from django.forms.widgets import RadioSelect, Textarea
from django.core.exceptions import ValidationError
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



# quizform should validate against create, progress marking 
class QuizCUForm(CleanUrlMixin, forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'

    def clean_url(self):
        new_url = (self.cleaned_data['url'].lower())
        if new_url == ['create', 'progress', 'marking', 'category', 'question']:
            raise ValidationError('You are not allowed to use this URL.')
        return new_url