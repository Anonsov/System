from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from .serializers import SubmissionSerializer, UpdateSubmissionSerializer
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Submission
from django.views.generic.list import ListView
from apps.problems.models import Problem
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.views.generic.detail import DetailView 
from .forms import ReadOnlyCodeForm
from rest_framework.generics import RetrieveUpdateAPIView
# from runner.base import Runner


# Create your views here.


class SubmissionsMainPageView(ListView):
    model = Submission
    paginate_by = 20
    template_name = "submissions/submissions.html"
    context_object_name = "submissions"
    ordering = ["-created_at"]
    
    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user).order_by("-created_at")


class SubmissionDetailView(DetailView):
    model = Submission
    template_name = "submissions/submission_detail.html"
    context_object_name = "submission"
    pk_url_kwarg = "submission_id"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        submission = self.get_object()
        form = ReadOnlyCodeForm(initial={'code_area': submission.code}) # type: ignore
        context['form'] = form
        return context
        

    
    
    
class NextPendingSubmissionAPIView(generics.RetrieveAPIView):
    serializer_class = SubmissionSerializer
    
    def get_object(self):
        submission = Submission.objects.filter(
            status=Submission.Status.PENDING
        ).order_by('created_at').first()
        
        if submission is None:
            return None
        return submission

    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance is None:
            return Response(
                {"detail": "No pending submissions found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        

class UpdateSubmissionAPIView(generics.RetrieveUpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = UpdateSubmissionSerializer 
    lookup_field = "id"
    
