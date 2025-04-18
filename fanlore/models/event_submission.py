import cloudinary.models
from django.conf import settings
from django.db import models

from .event import Event


class EventSubmission(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              related_name="submissions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    text_response = models.TextField(blank=True)
    file_upload = cloudinary.models.CloudinaryField(
        "file",
        folder="event_submissions/",
        blank=True,
        null=True,
        resource_type="auto"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.user.username} → {self.event.title}"
