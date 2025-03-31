from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe

from .models import User, Tag


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "bio",
                "profile_image",
                "followed_fandoms",
                "is_creator",
                "profile_background_image"
            )
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "fields": (
                "bio",
                "profile_image",
                "followed_fandoms",
                "is_creator",
                "profile_background_image"
            )
        }),
    )
    list_display = (
        "username",
        "email",
        "is_creator",
        "bio",
        "profile_image_preview",
    )
    search_fields = ("username", "email", "bio")

    def profile_image_preview(self, obj):
        """Show a small preview of the profile image in Django Admin"""
        if obj.profile_image and obj.profile_image.url:
            return mark_safe(
                f'<img src="{obj.profile_image.url}" width="50" height="50" '
                f'style="border-radius:50%; object-fit: cover;" '
                f'onerror="this.onerror=null; this.src=\'/static/fanlore/images/user-circle.png\'" />'
            )
        return "No Image"

    profile_image_preview.short_description = "Profile Image"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("-created_at",)

admin.site.register(User, CustomUserAdmin)
