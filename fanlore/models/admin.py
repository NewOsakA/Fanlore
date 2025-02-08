from django.db import models
from .user import User


class Admin(User):
    managed_events = models.JSONField(default=list)

    def __str__(self):
        return self.username
