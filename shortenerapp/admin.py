from django.contrib import admin
from .models import MyUsers, Urls
# Register your models here.
@admin.register(Urls)
class UrlsAdmin(admin.ModelAdmin):
    list_display = ["inUrl","outSlug"]

@admin.register(MyUsers)
class MyUsersAdmin(admin.ModelAdmin):
    list_display = ["userName","userEmail"]