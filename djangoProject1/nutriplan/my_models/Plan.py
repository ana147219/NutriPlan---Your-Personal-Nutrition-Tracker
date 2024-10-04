"""
Radovan Jevirc 0138/2021
"""
from django.db import models
from nutriplan.my_models.MyUser import MyUser
from nutriplan.my_models.Tag import Tag


class Plan(models.Model):
    """
    Plan is class that represents one food plan, it has its
    owner and it has name of the plan, also there is field
    that specifies is that plan public, so if it is public
    everybody should search that plan and found it
    """


    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=100, default="Plan Name",
        null=False, blank=False
    )
    owner = models.ForeignKey(
        MyUser, on_delete=models.RESTRICT,
        null=False, blank=False,
        help_text="User that is owner of the plan and only he can change it"
    )
    is_public = models.BooleanField(
        default=False,
        null=False, blank=False,
        help_text="Is this plan public?"
    )
    duration = models.PositiveIntegerField(
        default=1,
        null=False, blank=False,
        help_text="duration of the plan in days"
    )
    tags = models.ManyToManyField(
        Tag, through='HasTag',
        related_name="plans"
    )
