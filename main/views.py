from django.http.response import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from django.views.generic import TemplateView
from quiz.models import Category

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

def category_detail(request):
    category = category.objects.get(slug__iexact=url)
    template = loader.get_template(
        'quiz/category_detail.html')
    context = Context({'category': category})
    return HttpResponse(template.render(context))
