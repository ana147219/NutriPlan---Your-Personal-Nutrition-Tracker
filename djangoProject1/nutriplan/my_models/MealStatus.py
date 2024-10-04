"""
Radovan Jevric 0138/2021
"""

from django.db import models
from django.db.models import UniqueConstraint

from nutriplan.my_models.DayHistory import DayHistory
from nutriplan.my_models.Meal import Meal


class MealStatus(models.Model):
    """
    Used for following specified user his plan
    and history but on a meal level
    """

    day_history = models.ForeignKey(
        DayHistory, on_delete=models.RESTRICT,
        null=False, blank=False,
        help_text="on which day meal is taken or should be taken"
    )
    meal = models.ForeignKey(
        Meal, on_delete=models.RESTRICT,
        null=False, blank=False,
        help_text="what meal is taken or should be taken"
    )
    status = models.BooleanField(
        null=False, blank=False,
        default=False,
        help_text="is user following his plan"
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['day_history', 'meal'], name="unique_mealstatus"),
        ]
