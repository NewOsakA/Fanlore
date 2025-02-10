from django.db import models


class Category(models.IntegerChoices):
    GENERIC = 1, 'Generic'
    GAMES = 2, 'Games'
    FANART = 3, 'FanArt'
    LORE = 4, 'Lore'
    VIDEO = 5, 'Video'

    def __str__(self):
        return self.label  # Returns the display name of the choice
