from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
import cloudinary.models


class Event(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=300, blank=True)
    banner_image = cloudinary.models.CloudinaryField(
        "image",
        folder="event_banners/",
        blank=True,
        null=True
    )
    description = MarkdownField(rendered_field='description_rendered',
                                validator=VALIDATOR_STANDARD)
    description_rendered = RenderedMarkdownField()
    submission_start = models.DateTimeField(blank=True, null=True)
    submission_end = models.DateTimeField(blank=True, null=True)
    allow_text = models.BooleanField(default=True)
    allow_file = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    show_submissions = models.BooleanField(default=False)

    def is_open(self):
        now = timezone.now()
        if self.submission_start and self.submission_end:
            return self.submission_start <= now <= self.submission_end
        return True

    def has_started(self):
        if self.submission_start:
            return timezone.now() >= self.submission_start
        return True

    def has_ended(self):
        if self.submission_end:
            return timezone.now() > self.submission_end
        return False

    def get_absolute_url(self):
        return reverse("event-detail", args=[str(self.pk)])

    def __str__(self):
        return self.title
