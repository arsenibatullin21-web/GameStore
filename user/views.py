from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from user.forms import UserLoginForm, UserRegisterForm


class LoginUserView(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'
    success_url = reverse_lazy('main:home')

class RegisterUserView(CreateView):
    model = get_user_model()
    form_class = UserRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')

class ProfileUserView(DetailView):
    model = get_user_model()
    template_name = 'user/profile.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'
