"""
Natasa Spasic 0310/2021
"""

from django.db import models
from nutriplan.my_models.Form import Form
from nutriplan.my_models.Tag import Tag


class FormTags(models.Model):
    """
        Model that connects a form with all of her tags.
    """

    form = models.ForeignKey(
        Form, on_delete=models.CASCADE,
        help_text="If the form does not exist, then it can not have a tag"
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE,
        help_text="If the tag does not exist, then form can not have that tag"
    )