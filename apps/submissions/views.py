from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from .serializers import SubmissionSerializer
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Submission
from django.views.generic.list import ListView


# Create your views here.


class SubmissionsMainPageView(ListView):
    model = Submission
    paginate_by = 20
    template_name = "submissions/submissions.html"
    context_object_name = "submissions"
    ordering = ["-created_at"]
    
    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user).order_by("-created_at")


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
        

class UpdateSubmissionAPIView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    lookup_field = "id"
    
