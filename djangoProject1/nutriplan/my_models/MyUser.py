"""
Natasa Spasic 0310/2021
Tijana Gasic 0247/21
Radovan Jevric 0138/2021
Ana Vitkovic 0285/2021
"""


from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    """
    Class represents basic user of system
    """

    first_name = None
    last_name = None

    gender = models.CharField(
        max_length=1,
        choices=(('M', 'Male'), ('F', 'Female')),
        default="M",
        null=False,
        help_text="Gender of user"
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures',
        null=False,
        blank=False,
        default='default-user.jpg',
        help_text="Profile picture"
    )
    current_plan_index = models.IntegerField(
        null=False,
        blank=False,
        default=0,
    )
    following_plan = models.ForeignKey(
        "nutriplan.Plan", on_delete=models.SET_NULL, null=True,
    )