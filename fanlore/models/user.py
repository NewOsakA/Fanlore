import cloudinary.models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    display_name = models.CharField(max_length=150, blank=True, null=True)
    followed_fandoms = models.JSONField(default=list, null=True, blank=True)
    is_creator = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    profile_image = cloudinary.models.CloudinaryField(
        "image",
        folder="user_profile_image/",
        blank=True,
        null=True
    )
    profile_background_image = cloudinary.models.CloudinaryField(
        "image",
        folder="user_profile_background_image/",
        blank=True,
        null=True
    )
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)

    groups = models.ManyToManyField(Group, related_name="fanlore_user_groups",
                                    blank=True)
    user_permissions = models.ManyToManyField(Permission,
                                              related_name="fanlore_user_permissions",
                                              blank=True)

    def save(self, *args, **kwargs):
        if not self.display_name and self.first_name:
            self.display_name = self.first_name
        super().save(*args, **kwargs)
