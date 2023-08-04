from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Urls(models.Model):
    inUrl= models.URLField(blank=False)
    outSlug= models.SlugField(null=False,blank=False,unique=True)
    timer = models.IntegerField(default=1)
    isActive = models.BooleanField(default = 1)
    dateStarted = models.DateTimeField(default= timezone.now())
    isPublic = models.BooleanField(default= 1)
    ownerUser = models.ForeignKey(User, on_delete=models.CASCADE,related_name='owner',null=True)
    allowedUsers = models.ManyToManyField(User,related_name='allowed',)
    
    def __str__(self):
        return f"{self.outSlug}"