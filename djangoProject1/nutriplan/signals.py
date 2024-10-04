from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from nutriplan.my_models.Day import Day
from nutriplan.my_models.Plan import Plan

@receiver(post_save, sender=Day)
@receiver(post_delete, sender=Day)
def update_duration(sender, instance, **kwargs):
    plan = instance.plan
    plan.duration = Day.objects.filter(plan=plan).count()
    plan.save()
