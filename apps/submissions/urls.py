from django.urls import path, include
from . import views


app_name = "submissions"
urlpatterns = [
    path("", views.SubmissionsMainPageView.as_view(), name="SubmissionsMainPage")    
]