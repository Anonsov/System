from django.urls import path, include
from . import views


app_name = "submissions"
urlpatterns = [
    path("", views.NextPendingSubmissionAPIView.as_view())  ,
    path("submissions/next-pending/", views.NextPendingSubmissionAPIView.as_view()),
    path("submissions/<int:id>/update/", views.UpdateSubmissionAPIView.as_view()),
]