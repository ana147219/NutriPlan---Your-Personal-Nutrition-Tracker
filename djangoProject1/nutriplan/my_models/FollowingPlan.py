"""
Ana Vitkovic 0285/2021
"""

from django.db import models
from django.db.models import UniqueConstraint

from nutriplan.my_models.MyUser import MyUser
from nutriplan.my_models.Plan import Plan


class FollowingPlan(models.Model):

    """
    Traking downloaded plans for users
    """

    id_plan=models.ForeignKey(
        Plan, on_delete=models.CASCADE,
        help_text="If the plan does not exist, then it can not be followed"
    )
    id_user=models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        help_text="If the user does not exist, then it can not follow the plan"
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id_plan', 'id_user'], name='unique_following_plan')
        ]