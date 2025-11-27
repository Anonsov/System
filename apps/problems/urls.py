from django.urls import path

from . import views



app_name = "problems"

urlpatterns = [
    path('', views.ProblemListView.as_view(), name='ProblemsMainPage'),
    path('<slug:slug>/', views.ProblemDetailView.as_view(), name='simple_detail'),
    path('<slug:category_slug>/<slug:slug>/', views.ProblemDetailView.as_view(), name='detail'),
    
]