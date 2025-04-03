import uuid

from django.conf import settings
from django.db import models
from markdownfield.models import RenderedMarkdownField, MarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
from django.utils import timezone

from fanlore.models import Content


class Release(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    content = models.ForeignKey(
        Content, related_name="releases", on_delete=models.CASCADE
    )
    description = MarkdownField(rendered_field='description_rendered',
                                validator=VALIDATOR_STANDARD)
    description_rendered = RenderedMarkdownField()
    create_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def time_since_release(self):
        now = timezone.now()
        diff = now - self.create_at
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
        return f"Release for {self.content.title} by {self.updated_by.username}"
