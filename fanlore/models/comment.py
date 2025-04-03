from django.db import models
import uuid

from django.utils import timezone

from .content import Content


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          editable=False,
                          unique=True,
                          primary_key=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    commentator_name = models.CharField(max_length=255)
    comment_text = models.TextField()
    comment_at = models.DateTimeField(default=timezone.now, null=True)

    def time_since_comment(self):
        now = timezone.now()
        diff = now - self.comment_at
        total_seconds = diff.total_seconds()

        years = int(total_seconds // 31536000)
        months = int((total_seconds % 31536000) // 2592000)
        days = int((total_seconds % 2592000) // 86400)
        hours = int((total_seconds % 86400) // 3600)
        minutes = int((total_seconds % 3600) // 60)

        if years > 0:
            return f"{years} year{'s' if years > 1 else ''} ago"
        if months > 0:
            return f"{months} month{'s' if months > 1 else ''} ago"
        if days > 0:
            return f"{days} day{'s' if days > 1 else ''} ago"
        if hours > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        if minutes > 0:
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        return "Just now"

    def __str__(self):
        return f"Comment by {self.commentator_name}"
