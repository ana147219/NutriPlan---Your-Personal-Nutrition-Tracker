"""
Radovan Jevric 0138/2021
"""

from django.db import models
from django.db.models import UniqueConstraint

from nutriplan.my_models.MyUser import MyUser


class DayHistory(models.Model):
    """
    Class is use to track user specified meals, so
    every day in a plan becomes date, and also class is
    used to track history of user meals
    """

    data = models.DateField(
        auto_now=False, null=False,
        help_text="date of history"
    )
    user = models.ForeignKey(
        MyUser, on_delete=models.RESTRICT,
        null=False, blank=False,
        help_text="which user history is this"
    )
    plan_index = models.IntegerField(
        null=False, blank=False, default=0,
        help_text="used for following a progress of user in plan"
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['data', 'user'], name='unique_day_history'),
        ]