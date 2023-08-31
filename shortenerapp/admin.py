from django.contrib import admin
from .models import Urls
# Register your models here.
@admin.register(Urls)
class UrlsAdmin(admin.ModelAdmin):
    list_display = ["inUrl","outSlug", "ownerUser"]
