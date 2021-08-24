from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput

from .models import Project, ArticleLink


class CleanUrlMixin():
    """Mixin class for slug cleaning method."""

    def clean_url(self):
        new_slug = (self.cleaned_data['slug'].lower())
        if new_slug == 'create':
            raise ValidationError('URL may not be "create".')
        return new_slug


class ArticleLinkForm(CleanUrlMixin, forms.ModelForm):
    class Meta:
        model = ArticleLink
        fields = '__all__'
        widgets = {'project': HiddenInput()}


class ProjectForm(CleanUrlMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

