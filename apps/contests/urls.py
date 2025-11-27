from django.urls import path, include
from . import views

app_name = "contests"

urlpatterns = [
    path("", views.ContestsMainPageView.as_view(), name="ContestsMainPage")
]