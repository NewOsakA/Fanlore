import cloudinary.models
from django.db import models


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = cloudinary.models.CloudinaryField(
        "image",
        folder="achievement_icon/",
        blank=True,
        null=True
    )
    event = models.ForeignKey(
        "fanlore.Event",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="achievements"
    )

    def __str__(self):
        return self.name
