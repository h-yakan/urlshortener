from celery import shared_task
from celery.utils.log import get_task_logger
from urlshortener import settings
from .models import SendMail
from django.core.mail import send_mail
from celery.contrib import rdb


# @shared_task
# def countdown():
#     objects = Urls.objects.filter(isActive=1)
#     logger.info("Deneme1")
#     for obj in objects:
#         obj.timer = obj.timer - 1 
#         if obj.timer == 0:
#             obj.isActive = False
#         obj.save()

@shared_task(name="sendNotification")
def sendNotification(pk):
    obj = SendMail.objects.get(pk = pk)
    obj.done = 1
    obj.save()
    send_mail("Url'nizin kullanım süresi", obj.mailtext, from_email= "huseyin.yakan.sd@gmail.com", recipient_list = [obj.mail])