from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView 
from django.urls import reverse_lazy
from .forms import LoginUserForm, RegisterUserForm
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'
    extra_context = {'title': 'Авторизация'}
    
    
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('accounts:login')


class LogoutUser(LogoutView):
    next_page = '/'