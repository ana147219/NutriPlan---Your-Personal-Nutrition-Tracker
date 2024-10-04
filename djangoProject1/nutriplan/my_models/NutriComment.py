"""
Tijana Gasic 0247/2021
"""

from django.db import models
from nutriplan.my_models.Comment import Comment
from nutriplan.my_models.MyUser import MyUser


class NutriComment(Comment):
    """
    Model that represents comments that users posted for nutrtionists
    """

    def __str__(self):
        return super().__str__() + " ,   NUTRI: " + str(self.nutri.username)+ " => "+ str(self.text)

    nutri = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        null=False, blank=False,
        help_text=" Commments for nutritionist"
    )


    @property
    def author(self):
        return self.user.username

    @property
    def nutri_username(self):
        return self.nutri.username

    @property
    def comment(self):
        return super().text