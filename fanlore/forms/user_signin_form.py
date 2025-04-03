from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SignInForm(AuthenticationForm):
    """
    Form for user login, extending Django's built-in AuthenticationForm.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'}))
