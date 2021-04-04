from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from user.decorators import class_login_required, require_authenticated_permission, master_required
from main.utils import ArticleLinkGetObjectMixin, PageLinksMixin, ProjectContextMixin
from .models import Project, ArticleLink
from .forms import ArticleLinkForm, ProjectForm


# Create your views here.
class ProjectDetail(DetailView):
    model = Project

class ProjectList(PageLinksMixin, ListView):
    page_kwarg = 'page'
    paginate_by = 12 # 5 items per page
    template_name = 'projects/project_list.html'
    model = Project


@method_decorator([login_required, master_required], name='dispatch')
class ProjectCreate(CreateView):
    form_class = ProjectForm
    template_name = 'projects/project_create_form.html'


@method_decorator([login_required, master_required], name='dispatch')
class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('project:project_list')
    template_name = 'projects/project_confirm_delete.html'


@method_decorator([login_required, master_required], name='dispatch')
class ProjectUpdate(UpdateView):
    form_class = ProjectForm
    model = Project
    template_name = 'projects/project_update_form.html'


@method_decorator([login_required, master_required], name='dispatch')
class ArticleLinkCreate(ArticleLinkGetObjectMixin, ProjectContextMixin, CreateView):
    form_class = ArticleLinkForm
    template_name = 'projects/article_create_form.html'

    def get_initial(self):
        project_slug = self.kwargs.get(self.project_slug_url_kwarg)
        self.project = get_object_or_404(Project, slug__iexact=project_slug)
        initial = {self.project_context_object_name: self.project,}
        initial.update(self.initial)
        return initial


@method_decorator([login_required, master_required], name='dispatch')
class ArticleUpdate(ArticleLinkGetObjectMixin, ProjectContextMixin, UpdateView):
    form_class = ArticleLinkForm
    model = ArticleLink
    template_name = 'projects/article_update_form.html'
    slug_url_kwarg = 'articlelink_slug'


@method_decorator([login_required, master_required], name='dispatch')
class ArticleDelete(ArticleLinkGetObjectMixin, ProjectContextMixin, DeleteView):
    model = ArticleLink
    template_name = 'projects/article_confirm_delete.html'
    slug_url_kwarg = 'articlelink_slug'

    def get_success_url(self):
        return (self.object.project.get_absolute_url())
