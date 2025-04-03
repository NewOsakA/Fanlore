from django.db import models
from django.conf import settings
from .content import Content


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure each user can bookmark a post only once
        unique_together = ('user', 'content')

    def __str__(self):
        return f"{self.user.username} bookmarked {self.content.title}"
