import cloudinary.uploader
from django import forms

from ..models import User


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile, including password change and image upload.
    """

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

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "bio",
                  "profile_image"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password1 = self.cleaned_data.get("new_password1")
        profile_image = self.cleaned_data.get("profile_image")

        if new_password1:
            user.set_password(new_password1)

        if profile_image:
            public_id = f"user_profile_image/{user.id}"
            cloudinary.uploader.destroy(public_id)

            uploaded_image = cloudinary.uploader.upload(
                profile_image,
                folder="user_profile_image/",
                public_id=str(user.id),
                overwrite=True,
                resource_type="image"
            )

            user.profile_image = uploaded_image['secure_url']

        if commit:
            user.save()
        return user
