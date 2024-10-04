"""
Ana Vitkovic 0285/2021
"""

from django.db import models
from nutriplan.my_models.MyUser import MyUser

class RateNutri(models.Model):

    """
    Users are able to rate nutritionists so that nutritionists can be ranked by grade;
    grades provide great recommendation for those who are well ranked and also helps users
    to choose nutritionist based on other users' experience
    """

    id_nutricionist = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        related_name='rated_by',
        help_text="If nutricionist does not exist, then it can not be rated"
    )
    id_user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        related_name='rates_given',
        help_text="If the user does not exist, then it can not give a grade"
    )
    score=models.PositiveIntegerField(
        default=0,
        help_text="grade"
    )
