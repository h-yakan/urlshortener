from django.utils import timezone
from django.db import models

# Create your models here.
class MyUsers(models.Model):
    userName= models.TextField()
    userEmail= models.EmailField()

    def __str__(self):
        return f"{self.userEmail}"
    

class Urls(models.Model):
    inUrl= models.URLField(blank=False)
    outSlug= models.SlugField(null=False,blank=False,unique=True)
    timer = models.IntegerField(default=1)
    isActive = models.BooleanField(default = 1)
    dateStarted = models.DateTimeField(default= timezone.now())
    isPublic = models.BooleanField(default= 1)
    allowedUsers = models.ManyToManyField(MyUsers)

