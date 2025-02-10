from django.db import models
import uuid
from .comment import Comment
from .category import Category
from .user import User


class Content(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    topic_img = models.FileField(upload_to='content_images/')
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, blank=True)
    category = models.IntegerField(choices=Category.choices, default=Category.GENERIC)

    def __str__(self):
        return self.title
