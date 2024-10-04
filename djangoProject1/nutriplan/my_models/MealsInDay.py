"""
Radovan Jevirc 0138/2021
"""
from django.db import models
from nutriplan.my_models.Day import Day
from nutriplan.my_models.Meal import Meal
class MealsInDay(models.Model):
    """
    This class is helper class for saving meals,
    and it is here because it is possible to delete
    day and meals can be saved, but if this table would not
    exist we would need to have foreign key that is null in
    :model:'Meal'
    """

    day = models.ForeignKey(Day, on_delete=models.RESTRICT)
    meal = models.OneToOneField(Meal, on_delete=models.RESTRICT, primary_key=True)
