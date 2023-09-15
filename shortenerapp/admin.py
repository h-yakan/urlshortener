from django.contrib import admin
from .models import SendMail, Urls
# Register your models here.
@admin.register(Urls)
class UrlsAdmin(admin.ModelAdmin):
    list_display = ["inUrl","outSlug", "ownerUser", "timer"]

@admin.register(SendMail)
class SendMailAdmin(admin.ModelAdmin):
    list_display = ["mail","sendingDate","done","status","task"]
