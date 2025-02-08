from django.db import models
import uuid
from .fandom import Fandom
from .creator import Creator
from .content import Content


class Report(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    reason = models.TextField()
    reported_by = models.ForeignKey(Fandom, null=True, blank=True, on_delete=models.SET_NULL)
    reported_by_creator = models.ForeignKey(Creator, null=True, blank=True, on_delete=models.SET_NULL)
    reported_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report on {self.content.title} by {self.reported_by.username if self.reported_by else self.reported_by_creator.username}"
