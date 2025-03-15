from django import forms
from django.contrib.auth.forms import UserCreationForm
from fanlore.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    """
    Form for user registration, extending Django's built-in UserCreationForm.
    Includes additional validation for unique usernames and emails.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        """
        Validates that the username is unique.
        Raises a ValidationError if the username is already taken.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose a different one.")
        return username

    def clean_email(self):
        """
        Validates that the email is unique.
        Raises a ValidationError if the email is already registered.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use a different email.")
        return email

    def clean(self):
        """
        Ensures that the two password fields match.
        Raises a ValidationError if the passwords do not match.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")
        return cleaned_data
