from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    """Custom login form with styled inputs."""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class CustomLoginView(LoginView):
    """Login view using Django's built-in authentication system."""
    template_name = "login.html"
    form_class = CustomLoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy("home")
