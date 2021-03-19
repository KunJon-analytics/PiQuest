from django.http.response import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'


