import uuid
import cloudinary.models
from django.utils import timezone
from django.conf import settings
from django.db import models
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
from .tag import Tag

from .category import Category


class Content(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    description = MarkdownField(rendered_field='description_rendered',
                                validator=VALIDATOR_STANDARD)
    description_rendered = RenderedMarkdownField()
    topic_img = cloudinary.models.CloudinaryField(
        "image",
        folder="content_images/",
        blank=True,
        null=True
    )
    collaborator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    category = models.IntegerField(choices=Category.choices, default=Category.GENERIC)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    create_at = models.DateTimeField(default=timezone.now, null=True)

    def time_since_creation(self):
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
        return self.title

class ContentFile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    content = models.ForeignKey(
        Content,
        related_name='attached_files',
        on_delete=models.CASCADE
    )
    file = cloudinary.models.CloudinaryField(
        "file",
        folder="content_files/",
        blank=True,
        null=True
    )
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"File {self.file.name} for {self.content.title}"
