"""
Ana Vitkovic 0285/2021
"""

from django.db import models
from nutriplan.my_models.Plan import Plan
from nutriplan.my_models.Tag import Tag


class HasTag(models.Model):

    """
    Plans can have multiple tags which allows users search based on their interests
    """

    plan=models.ForeignKey(
        Plan, on_delete=models.CASCADE,
        help_text="If the plan does not exist, then it can not have a tag"
    )
    tag=models.ForeignKey(
        Tag, on_delete=models.CASCADE,
        help_text="If the tag does not exist, then plan can not have that tag"
    )