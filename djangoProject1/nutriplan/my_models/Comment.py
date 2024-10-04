
"""
Tijana Gasic 0247/2021
"""

from django.db import models
from nutriplan.my_models.MyUser import MyUser


class Comment(models.Model):

    """
    Model for Comments that users post
    """


    def __str__(self):
        return "AUTHOR: " + str(self.user.username)

    user=models.ForeignKey(

        MyUser, on_delete=models.CASCADE,
        null=False, blank=False,
        help_text=" User that commented"
    )


    text=models.CharField(
        max_length=500, null=False, blank=False,
        default="",
        help_text=" Comment content"


    )

    @property
    def comment(self):
        return self.text