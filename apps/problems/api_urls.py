from django.urls import path
from django.shortcuts import render
from .views import ProblemsAPIView

urlpatterns = [
    path("problemlist/", ProblemsAPIView.as_view()),
]