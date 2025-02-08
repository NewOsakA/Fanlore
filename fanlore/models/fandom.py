from django.db import models
from .user import User


class Fandom(User):
    followed_fandoms = models.JSONField(default=list)

    def __str__(self):
        return self.username

