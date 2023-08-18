from celery import shared_task
from .models import Urls

@shared_task
def countdown():
    objects = Urls.objects.filter(isActive=1)
    for obj in objects:
        obj.timer -= obj.timer
        if obj.timer == 0:
            obj.isActive = False
        obj.save()