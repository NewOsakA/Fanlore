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
    condition_code = models.CharField(max_length=100)  # optional: for logic matching

    def __str__(self):
        return self.name
