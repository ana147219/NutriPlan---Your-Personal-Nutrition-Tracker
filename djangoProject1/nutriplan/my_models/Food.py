"""
Radovan Jevric 0138/2021
"""

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Food(models.Model):

    def __str__(self):
        return self.name

    """
    Class representing a Food model
    """

    L = "l"
    G = "g"
    A = "a"
    UNIT_CHOICES = {
        L: "liters",
        G: "grams",
        A: "amount"
    }

    FRUIT = "fr"
    VEGETABLES = "vg"
    MEET = "mt"
    CEREAL = "cr"
    FISH = "fi"
    PASTRY = "ps"
    DISHES = "ds"
    NUTS = "nu"
    SWEET = "sw"
    DRINKS = "dr"

    FOOD_TYPE_CHOICES = {
        FRUIT: "fruit",
        VEGETABLES: "vegetables",
        MEET: "meat",
        CEREAL: "cereal",
        FISH: "seafood",
        PASTRY: "pastry",
        DISHES: "dishes",
        NUTS: "nuts",
        SWEET: "sweet",
        DRINKS: "drinks",
    }

    name = models.CharField(
        max_length=100, null=False, blank=False
    )
    calories = models.DecimalField(
        max_digits=5, decimal_places=2, 
        null=False, blank=False,
        help_text="number of calories that food have in 100g"
    )
    protein = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=False, blank=False,
        help_text="number of proteins that food have in 100g"
    )
    fiber = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=False, blank=False,
        help_text="number of fibers that food have in 100g"
    )
    fat = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=False, blank=False,
        help_text="number of fats that food have in 100g"
    )
    carbs = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=False, blank=False,
        help_text="number of carbs that food have in 100g"
    )
    sugar = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=False, blank=False,
        help_text="number of sugar that food have in 100g"
    )
    food_picture = models.ImageField(
        upload_to='food_pictures', 
        null=False, blank=False,
    )
    unit = models.CharField(
        max_length=1, choices=UNIT_CHOICES.items(),
        default=G, null=False, blank=False,
        help_text="unit that food can have in meal"
    )
    food_type = models.CharField(
        max_length=2, choices=FOOD_TYPE_CHOICES.items(), default=FRUIT,
        null=False, blank=False,
        help_text="type of food used for faster searching"
    )