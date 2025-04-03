import uuid
import cloudinary.models
from django.db import models
from django.utils import timezone


class File(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    file = cloudinary.models.CloudinaryField(
        "file",
        folder="content_files/",
        blank=True,
        null=True
    )
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def __str__(self):
        return f"File {self.file.name} uploaded at {self.uploaded_at}"


class ContentFile(File):
    content = models.ForeignKey(
        'fanlore.Content',
        related_name='attached_files',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"File {self.file.name} for {self.content.title}"


class ReleaseFile(File):
    release = models.ForeignKey(
        'fanlore.Release',
        related_name='release_files',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"File {self.file.name} for release {self.release.title}"