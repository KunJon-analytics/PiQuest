from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView, ListView, TemplateView, FormView, View
from .models import Project, ArticleLink
from .forms import ArticleLinkForm, ProjectForm

# Create your views here.
def project_detail(request, url):
    project = get_object_or_404(Project, url__iexact=url)
    return render(request, 'projects/project_detail.html', {'project': project})


class ProjectList(View):

    def get(self, request):
        return render(request, 'projects/project_list.html', {'project_list': Project.objects.all()})


class ArticleLinkCreate(View):
    form_class = ArticleLinkForm
    template_name = 'projects/article_create_form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_article = bound_form.save()
            return redirect(new_article)
        else:
            return render(request, self.template_name,{'form': bound_form})


class ProjectCreate(View):
    form_class = ProjectForm
    template_name = 'projects/project_create_form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_project = bound_form.save()
            return redirect(new_project)
        else:
            return render(request, self.template_name,{'form': bound_form})