from django.urls import path
from . import views

app_name = "archive"

urlpatterns = [
    path("", views.ArchiveMainPageView.as_view(), name="ArchiveMainPage"),
    path("section/<slug:slug>", views.ArchiveSectionDetailView.as_view(), name="ArchiveSectionDetail")
]