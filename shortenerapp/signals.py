

from django.dispatch import receiver
from shortenerapp import models
from shortenerapp.enums import SendMailStatus
from django.db.models.signals import post_save

@receiver(post_save, sender=models.SendMail)
def create_or_update_periodic_task(sender, instance, created, **kwargs):
    if created:
        instance.setup_task()
    else:
        if instance.task is not None:
            instance.task.enabled = instance.status == SendMailStatus.active
            instance.task.save()