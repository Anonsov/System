from django.urls import path
from django.shortcuts import render
from .views import ProblemsAPIView, NextPendingSubmissionAPIView, UpdateSubmissionAPIView


urlpatterns = [
    path("problemlist/", ProblemsAPIView.as_view()),
    path("next-pending/", NextPendingSubmissionAPIView.as_view()),
    path("submissions/<int:id>/update/", UpdateSubmissionAPIView.as_view())
]