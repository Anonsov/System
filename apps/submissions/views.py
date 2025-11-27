from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class SubmissionsMainPageView(TemplateView):
    template_name = "submissions/submissions.html"