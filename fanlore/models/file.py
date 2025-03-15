from django.db import models
from .content import Content


class File(models.Model):
    content = models.ForeignKey(Content, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='content_files/')
    description = models.TextField(null=True)

    def __str__(self):
        return self.file.name
