from django.urls import path, include
from . import views


app_name = "submissions"

urlpatterns = [
    path("", views.SubmissionsMainPageView.as_view(), name="SubmissionsMainPage"),
    path("run/<int:submission_id>", views.SubmissionDetailView.as_view(), name="RunSubmission")
]