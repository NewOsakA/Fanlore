import cloudinary.models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    display_name = models.CharField(max_length=150, blank=True, null=True)
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
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True
    )
    friends = models.ManyToManyField("self",
                                     symmetrical=True,
                                     blank=True)

    groups = models.ManyToManyField(Group,
                                    related_name="fanlore_user_groups",
                                    blank=True)
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="fanlore_user_permissions",
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.display_name and self.first_name:
            self.display_name = self.first_name
        super().save(*args, **kwargs)

    # Check if the user is following another user
    def is_following(self, user):
        return self.following.filter(pk=user.pk).exists()

    # Follow another user
    def follow(self, user):
        if user != self and not self.is_following(user):
            self.following.add(user)

    # Unfollow a user
    def unfollow(self, user):
        if user != self and self.is_following(user):
            self.following.remove(user)

    # Get the number of followers
    def follower_count(self):
        return self.followers.count()

    # Get the number of following
    def following_count(self):
        return self.following.count()
