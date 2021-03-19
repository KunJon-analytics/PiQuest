from django import forms
from django.core.exceptions import ValidationError

from .models import Project, ArticleLink


class CleanUrlMixin():
    """Mixin class for url cleaning method."""

    def clean_url(self):
        new_url = (self.cleaned_data['url'].lower())
        if new_url == 'create':
            raise ValidationError('URL may not be "create".')
        return new_url


class ArticleLinkForm(forms.ModelForm):
    class Meta:
        model = ArticleLink
        fields = '__all__'


class ProjectForm(CleanUrlMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

    
