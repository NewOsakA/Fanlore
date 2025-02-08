from django.db import models
from .user import User
from .badge import Badge
from .content import Content


class Creator(User):
    followed_fandoms = models.JSONField(default=list)
    badges = models.ManyToManyField(Badge, related_name="creators")
    contents = models.ManyToManyField(Content, related_name="creators")

    def __str__(self):
        return self.username
