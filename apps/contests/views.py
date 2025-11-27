from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class ContestsMainPageView(TemplateView):
    template_name = "contests/contests.html"
