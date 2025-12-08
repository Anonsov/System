from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic import ListView
from django.contrib.auth.views import LoginView 
from django.urls import reverse_lazy
from .forms import LoginUserForm, RegisterUserForm, AvatarUpdateForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import Profile


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

    def form_valid(self, form):
        user = form.save()
        profile, created = Profile.objects.get_or_create(user=user)
        avatar = form.cleaned_data.get('avatar')
        if avatar:
            profile.avatar = avatar
            profile.save()
        
        return redirect(self.success_url)


class LogoutUser(LogoutView):
    next_page = '/'
    
    
class ProfileView(ListView):
    model = Profile
    template_name = "accounts/profile.html"
    
    def get(self, request, *args, **kwargs):
        form = AvatarUpdateForm(instance=request.user.profile) #type: ignore
        return render(request, self.template_name, {'form': form, 'user': request.user})

    def post(self, request, *args, **kwargs):
        form = AvatarUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
        return redirect('accounts:profile')
        