"""
Ana Vitkovic 0285/2021
"""

from django.db import models

class Tag(models.Model):
    """
    Tags represent the keywords which are assigned to the plans to help with the search
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name