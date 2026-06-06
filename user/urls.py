from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from user import views

app_name='user'

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('profile/<int:user_id>', views.ProfileUserView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='main:home'), name='logout'),
]