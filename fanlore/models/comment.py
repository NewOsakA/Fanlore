from django.db import models
import uuid


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    commentator_name = models.CharField(max_length=255)
    comment_text = models.TextField()

    def __str__(self):
        return f"Comment by {self.commentator_name}"
