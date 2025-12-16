from typing import Any
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.contrib import messages
from django.db.models import Exists, OuterRef
from .forms import CodeForm
from .models import Problem
from apps.submissions.models import Submission
from rest_framework import generics
from .serializers import ProblemSerializer
from apps.submissions import tasks as submission_tasks

class ProblemListView(ListView):
    model = Problem
    paginate_by = 20
    template_name = "problems/problems.html"
    context_object_name = "problems"
    ordering = ['-created_at']
    
    
    def get_queryset(self):
        queryset = Problem.objects.filter(is_hidden=False).order_by(*self.ordering)
        q = self.request.GET.get('q')
        tag = self.request.GET.get('tag')
        difficulty = self.request.GET.get('difficulty')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if q:
            queryset = queryset.filter(title__icontains=q)
        if tag:
            queryset = queryset.filter(tags__id=tag)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        queryset = queryset.distinct()

        user = self.request.user
        if user.is_authenticated:
            base_sub_qs = Submission.objects.filter(user=user, problem=OuterRef("pk"))

            queryset = queryset.annotate(
                is_tried=Exists(base_sub_qs),
                is_solved=Exists(base_sub_qs.filter(status=Submission.Status.ACCEPTED)),
            )
        else:
            none = Submission.objects.none()
            queryset = queryset.annotate(
                is_tried=Exists(none),
                is_solved=Exists(none),
            )

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.problems.models import Tag
        context['tags'] = Tag.objects.all()
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
        user = self.request.user
        problem = self.object

        if user.is_authenticated:
            qs = Submission.objects.filter(user=user, problem=problem)
            context["is_tried"] = qs.exists()
            context["is_solved"] = qs.filter(status=Submission.Status.ACCEPTED).exists()
        else:
            context["is_tried"] = False
            context["is_solved"] = False
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
            submission_tasks.judge_submission.apply_async((submission.id,), queue="judge") #type: ignore

            messages.success(request, f'Решение отправлено под ID: {submission.id}')
            
            return redirect(reverse('submissions:RunSubmission', args=[submission.id]))
        else:
            return self.form_invalid(form)
        
        

        
class ProblemsAPIView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer