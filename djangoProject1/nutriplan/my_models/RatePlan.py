"""
Ana Vitkovic 0285/2021
"""

from django.db import models
from nutriplan.my_models.MyUser import MyUser
from nutriplan.my_models.Plan import Plan

class RatePlan(models.Model):

    """
    Users are able to rate plans so that plans can be ranked by grade,
    grades provide great recommendation for those plans which are well ranked
    """

    id_plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE,
        help_text="If the plan does not exist, then it can not be rated"
    )
    id_user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        help_text="If the user does not exist, then it can not rate the plan"
    )
    score=models.PositiveIntegerField(
        default=0,
        help_text="grade"
    )
