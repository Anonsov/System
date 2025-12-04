from typing import Any
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.contrib import messages
from .forms import CodeForm
from .models import Problem
from apps.submissions.models import Submission
from rest_framework import generics
from .serializers import ProblemSerializer


class ProblemListView(ListView):
    model = Problem
    paginate_by = 20
    template_name = "problems/problems.html"
    context_object_name = "problems"
    ordering = ['-created_at']
    
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Problems'
        return context
    
    
class ProblemDetailView(FormMixin, DetailView):
    model = Problem
    template_name = 'problems/detail.html'
    context_object_name = 'problem'
    form_class = CodeForm
    
    
    def get_object(self):
        category_slug = self.kwargs.get('category_slug')
        slug = self.kwargs.get('slug')
        if category_slug:
            problem = Problem.objects.filter(
                slug=slug,
                tags__slug=category_slug
            ).first()
            
            if problem:
                return problem
            else:
                return get_object_or_404(Problem, slug=slug)
        else:
            return get_object_or_404(Problem, slug=slug)
        
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    
    def get_success_url(self) -> str:
        return reverse('problems:detail', kwargs={'category_slug': self.object.get_category_slug(),'slug': self.object.slug})
    
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        print(self)
        if form.is_valid():
            code = form.cleaned_data['code_area']
            language = request.POST.get('language', 'python')
            
            submission = Submission.objects.create(
                user=request.user,
                problem=self.object,
                code=code,
                language=language,
                status=Submission.Status.PENDING
            )
            messages.success(request, f'Решение отправлено под ID: {submission.id}')
            
            
            #TODO: Process the submission (run and etc things)        
        
            return redirect(reverse('submissions:RunSubmission', args=[submission.id]))
        else:
            return self.form_invalid(form)
        
        

        
class ProblemsAPIView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer