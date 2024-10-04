"""
Radovan Jevric 0138/2021
"""


from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from nutriplan.my_models.Day import Day
from nutriplan.my_models.Food import Food
class Meal(models.Model):
    """
    This class represents a Meal object.
    And it is connected to a day, so for every meal
    we know which day and in what hour, and how much
    that meal should be eaten. Meal is also connected to
    the :model:'Food'
    """

    amount = models.PositiveIntegerField(
        null=False, blank=False, default=100,
        help_text="How much you should eat"
    )
    hour = models.IntegerField(
        null=False, blank=False, default=0,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="When should u eat your meal"
    )
    food = models.ForeignKey(
        Food,
        on_delete=models.RESTRICT,
        help_text="What food do you want to eat"
    )
    day = models.ManyToManyField(
        Day, through="MealsInDay",
        help_text="What day is reserved for this meal"
    )
