from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe

from .models import User, Tag, UserAchievement, Achievement, Content, Report


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "bio",
                "display_name",
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
                "display_name",
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
        "display_name",
        "is_creator",
        "bio",
        "profile_image_preview",
    )
    search_fields = ("username", "email", "bio")

    def profile_image_preview(self, obj):
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


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "topic_img", "creator", "display_collaborators",
                    "vote", "category", "display_tags", "create_at")
    search_fields = ("title", "creator__display_name")
    ordering = ("-create_at",)

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    def display_collaborators(self, obj):
        return ", ".join(user.username for user in obj.collaborators.all())

    display_collaborators.short_description = "Collaborators"
    display_tags.short_description = "Tags"


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ("user", "achievement", "date_earned")
    search_fields = ("user__username", "achievement__name")
    list_filter = ("achievement", "date_earned")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("content", "content_creator", "topic", "reported_by", "reported_date")
    readonly_fields = ("content", "content_creator", "topic", "reason", "reported_by", "reported_date")
    fieldsets = (
        (None, {
            "fields": ("content", "content_creator", "topic", "reason", "reported_by", "reported_date")
        }),
    )

    def content_creator(self, obj):
        return obj.content.creator.username if obj.content and obj.content.creator else "Unknown"
    content_creator.short_description = "Content Creator"

    def has_add_permission(self, request):
        return False  # disable add

    def has_change_permission(self, request, obj=None):
        return False  # disable editing

    def has_delete_permission(self, request, obj=None):
        return True  # still allow delete if you want

# Register custom UserAdmin
admin.site.register(User, CustomUserAdmin)
