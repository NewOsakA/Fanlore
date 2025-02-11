from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    followed_fandoms = models.JSONField(default=list)
    is_creator = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="fanlore_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="fanlore_user_permissions", blank=True)
