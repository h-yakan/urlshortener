
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path






urlpatterns = [
    path('', include('shortenerapp.urls')),
    path('admin/', admin.site.urls),
]
