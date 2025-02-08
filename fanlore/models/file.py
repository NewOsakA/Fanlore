from django.db import models


class File(models.Model):
    file = models.FileField(upload_to='content_files/')
    description = models.TextField()

    def __str__(self):
        return self.description
