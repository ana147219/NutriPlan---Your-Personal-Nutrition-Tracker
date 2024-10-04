"""
Radovan Jevric 0138/2021
"""

from django.db import models
from django.db.models import UniqueConstraint
from nutriplan.my_models.Plan import Plan


class Day(models.Model):
    """
    Class represents one day in specific :model:'Plan'
    Day consist of :model:'Meal'
    """
    plan = models.ForeignKey(
        Plan, on_delete=models.RESTRICT,
        help_text="for which plan is this day connected"
    )
    day_number = models.PositiveSmallIntegerField(
        help_text="what day is this day in plan"
    )
    class Meta:
        constraints = [
            UniqueConstraint(fields=['plan', 'day_number'], name='unique_day'),
        ]
