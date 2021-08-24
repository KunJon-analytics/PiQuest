from django import forms
from django.forms.utils import ValidationError
from .models import MCQuestion


class MCQAddForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off'}))

    class Meta:
        model = MCQuestion
        fields = ('figure', 'content', 'explanation', 'answer_order')


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError(
                'Mark at least one answer as correct.', code='no_correct_answer')
