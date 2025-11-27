from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class ArchiveMainPageView(TemplateView):
    template_name = "archive/archive.html"
    
