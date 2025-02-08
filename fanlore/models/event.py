from django.db import models
from .admin import Admin
from .user import User


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    created_by = models.ForeignKey(Admin, on_delete=models.CASCADE)
    participants = models.ManyToManyField('Creator')

    def __str__(self):
        return self.name
