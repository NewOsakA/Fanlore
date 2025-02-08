from django.db import models


class Category(models.IntegerChoices):
    TECHNOLOGY = 1, 'Technology'
    ART = 2, 'Art'
    ENTERTAINMENT = 3, 'Entertainment'
    SCIENCE = 4, 'Science'
    LITERATURE = 5, 'Literature'

    def __str__(self):
        return self.get_display_name()
