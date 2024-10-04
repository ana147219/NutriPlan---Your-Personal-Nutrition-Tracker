"""
Natasa Spasic 0310/2021
"""

from django.core.validators import MinValueValidator
from django.db import models

from nutriplan.my_models.MyUser import MyUser
from nutriplan.my_models.Tag import Tag


class Form(models.Model):
    """
        Model for forms that user sends to nutritionist.
    """
    id_nutritionist = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        related_name='receive_form',
        help_text="If nutritionist does not exist, then form can not be submitted"
    )
    id_user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        related_name='sends_form',
        help_text="If the user does not exist, then it can not submit form"
    )
    height = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0,
        help_text="The height of the user"
    )
    weight = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0,
        help_text="The weight of the user"
    )
    description = models.TextField(
        max_length=500,
        help_text="The description of the user`s needs"
    )
    state = models.CharField(
        max_length=1,
        choices=(('N', 'New'), ('C', 'Created'), ('D', 'Dismissed')),
        default="N",
        null=False,
        help_text="State of form"
    )
    tags = models.ManyToManyField(
        Tag, through="FormTags",
        related_name='form_tags',
    )