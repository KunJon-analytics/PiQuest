from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, TemplateView, FormView, View
from .models import Project, ArticleLink

# Create your views here.
def project_detail(request, url):
    project = get_object_or_404(Project, url__iexact=url)
    return render(request, 'projects/project_detail.html', {'project': project})


# def project_list(request):
#     return render(request,'projects/project_list.html',{'project_list': Project.objects.all()})

# class ProjectListView(ListView):
#     model = Project


class ProjectList(View):

    def get(self, request):
        return render(request, 'projects/project_list.html', {'project_list': Project.objects.all()})

