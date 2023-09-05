import json
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from datetime import datetime, timedelta 
from django_enum_choices.fields import EnumChoiceField
from django.dispatch import receiver
from shortenerapp.enums import SendMailStatus
from django.db.models.signals import post_save

# Create your models here.


class Urls(models.Model):
    inUrl= models.URLField(blank=False,verbose_name="Kısaltmak istediğiniz URL'yi girin")
    outSlug= models.SlugField(null=False,blank=False,unique=True)
    timer = models.IntegerField(default=1,verbose_name="Kısa URL'niz kaç gün aktif olsun")
    expirationDate = models.DateTimeField(default=datetime.now(), blank=True)
    isActive = models.BooleanField(default = 1)
    dateStarted = models.DateTimeField(auto_now_add=True)
    isPublic = models.BooleanField(default= 1,verbose_name="URL'niz herkese açık olsun mu")
    ownerUser = models.ForeignKey(User, on_delete=models.CASCADE,related_name='owner',null=True)
    allowedUsers = models.ManyToManyField(User,related_name='allowed',)
    
    def __str__(self):
            return f"{self.outSlug}"
    
    def save(self,*args,**kwargs):
          self.expirationDate = self.expirationDate + timedelta(days=self.timer)
          super(Urls,self).save(*args,**kwargs)

class SendMail(models.Model):
      mail = models.EmailField(blank=False)
      mailtext = models.TextField(default="")
      sendingDate = models.DateTimeField(auto_now_add=True)
      done = models.BooleanField(default=False)
      status = EnumChoiceField(SendMailStatus, default=SendMailStatus.active)
      task = models.OneToOneField(
            PeriodicTask,
            on_delete=models.CASCADE,
            null=True,
            blank=True)
            
      def setup_task(self):
            pk = self.pk
            clocked, _ = ClockedSchedule.objects.get_or_create(
                  clocked_time = self.sendingDate)
            self.task = PeriodicTask.objects.create(
            name=self.mail + str(pk),
            task="sendNotification",
            clocked=clocked,
            kwargs = json.dumps({'pk':pk}),
            one_off=True,
            expires= self.sendingDate + timedelta(days=1),
            enabled = True,
            )
            self.save() 
      
      def delete(self, *args, **kwargs):
            if self.task is not None:
                  self.task.delete()
            return super(self.__class__, self).delete(*args, **kwargs)

@receiver(post_save, sender=SendMail)
def create_or_update_periodic_task(sender, instance, created, **kwargs):
    if created:
        instance.setup_task()
    else:
        if instance.task is not None:
            instance.task.enabled = instance.status == SendMailStatus.active
            instance.task.save()