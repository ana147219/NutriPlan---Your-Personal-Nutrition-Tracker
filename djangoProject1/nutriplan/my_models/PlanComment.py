
"""
Tijana Gasic 0247/2021
"""

from django.db import models

from nutriplan.my_models.Comment import Comment
from nutriplan.my_models.Plan import Plan


class PlanComment(Comment):
    """
    Model that represents comments that users posted for public plans
    """


    def __str__(self):
        return super().__str__() + " ,   PLAN: " + str(self.plan.name)+ " => "+ str(self.text)

    plan=models.ForeignKey(
        Plan, on_delete=models.CASCADE,
        null=False, blank=False,
        help_text=" Commments for plan"
    )


    @property
    def author(self):
        return self.user.username

    @property
    def plan_name(self):
        return self.plan.name

    @property
    def comment(self):
        return super().text