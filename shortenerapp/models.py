from django.db import models

# Create your models here.
class Urls(models.Model):
    inUrl= models.URLField(blank=False)
    outSlug= models.SlugField(null=False,blank=False,unique=True)