from django.db import models


class Badge(models.Model):
    """
    Model class for Achievements and badges
    """
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    criteria = models.CharField(max_length=255)
    receive_dated = models.DateTimeField()

    def __str__(self):
        return self.name
