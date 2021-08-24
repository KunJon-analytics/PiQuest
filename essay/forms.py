from django import forms
from .models import Essay_Question


class EssayAddForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off'}))

    class Meta:
        model = Essay_Question
        fields = ('figure', 'content', 'explanation')
