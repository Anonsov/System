from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from apps.accounts.models import Profile
from apps.problems.models import Problem

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leaderboard'] = Profile.objects.order_by('-score', '-solved_count')[:5]
        context['featured_problems'] = Problem.objects.order_by('-created_at')[:3]
        return context