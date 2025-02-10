from django.db import models
import uuid
from datetime import datetime


class User(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    joined_date = models.DateTimeField(default=datetime.now)
    followed_fandoms = models.JSONField(default=list)
    is_creator = models.BooleanField(default=False)
