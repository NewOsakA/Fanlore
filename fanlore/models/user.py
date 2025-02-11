from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    followed_fandoms = models.JSONField(default=list)
    is_creator = models.BooleanField(default=False)