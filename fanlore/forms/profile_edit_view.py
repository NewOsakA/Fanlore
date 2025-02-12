from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

from ..models import User


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile, including password change."""

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
        label="Current Password",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
        label="New Password",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
        label="Confirm New Password",
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name","email", "username"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email)\
                .exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username)\
                .exclude(pk=self.instance.pk).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 or new_password2:
            if not old_password:
                raise ValidationError(
                    "You must enter your current password to change it.")
            if not self.instance.check_password(old_password):
                raise ValidationError("The current password is incorrect.")
            if new_password1 and new_password2 and\
                    new_password1 != new_password2:
                raise ValidationError("New passwords do not match.")
            password_validation.validate_password(new_password1, self.instance)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password1 = self.cleaned_data.get("new_password1")

        if new_password1:
            user.set_password(new_password1)

        if commit:
            user.save()
        return user
