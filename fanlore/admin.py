from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": (
        "bio", "profile_image", "followed_fandoms", "is_creator")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": (
        "bio", "profile_image", "followed_fandoms", "is_creator")}),
    )
    list_display = (
    "username", "email", "is_creator", "bio", "profile_image_preview")
    search_fields = ("username", "email", "bio")

    def profile_image_preview(self, obj):
        """Show a small preview of the profile image in Django Admin"""
        if obj.profile_image and obj.profile_image.url:
            return mark_safe(
                f'<img src="{obj.profile_image.url}"'
                f' width="50" height="50" style="border-radius:50%;"'
                f' onerror="this.onerror=null; '
                f'this.src=\'/static/default-profile.png\'" />')
        return "No Image"

    profile_image_preview.short_description = "Profile Image"


admin.site.register(User, CustomUserAdmin)
