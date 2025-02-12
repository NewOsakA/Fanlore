import uuid

from django.conf import settings
from django.db import models

from .category import Category
from .comment import Comment


class Content(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,
                          primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    topic_img = models.FileField(upload_to='content_images/')
    collaborator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, blank=True)
    category = models.IntegerField(choices=Category.choices,
                                   default=Category.GENERIC)

    def __str__(self):
        return self.title
