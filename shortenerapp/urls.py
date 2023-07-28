
from django.urls import path
from . import views





urlpatterns = [
    path('save',views.saveUrl,name='save'),
    path('',views.index),
    path('<accessed_url>',views.shortenedRedirect)
]