from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError


class UserLoginForm(AuthenticationForm):
    username = UsernameField(max_length=100, required=True, label='Username')
    password = forms.CharField(required=True, label='Password')

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']



class UserRegisterForm(UserCreationForm):
    username = UsernameField(max_length=100, required=True, label='Username')
    password1 = forms.CharField(required=True, label='Password')
    password2 = forms.CharField(required=True, label='Repeat Password')

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email', 'phone', 'image']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            return ValidationError('Email is already taken!')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            return ValidationError("Username is already take!")
        return username


