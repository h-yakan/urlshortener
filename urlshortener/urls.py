
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path






urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shortenerapp.urls')),
    path('accounts/', include('allauth.urls')),
]
