from django import forms
from .models import TF_Question


class TFAddForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off'}))

    class Meta:
        model = TF_Question
        fields = ('figure', 'content', 'explanation', 'correct')
