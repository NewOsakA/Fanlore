from django import forms
from ..models import User


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile,
    including optional password change and image uploads.
    """

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
        label="Current Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
        label="Confirm New Password"
    )

    bio = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        required=False,
        label="Bio"
    )

    profile_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Profile Image"
    )

    profile_background_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Profile Background Image"
    )

    display_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Display Name"
    )

    class Meta:
        model = User
        fields = [
            "display_name", "first_name", "last_name",
            "email", "username", "bio",
            "profile_image", "profile_background_image"
        ]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        """
        Saves the user profile.
        Image fields are handled automatically by CloudinaryField.
        """
        user = super().save(commit=False)
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")

        if new_password1 and new_password1 == new_password2:
            user.set_password(new_password1)

        if commit:
            user.save()
        return user
