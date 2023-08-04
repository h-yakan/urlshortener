
from django.urls import path
from . import views





urlpatterns = [
    # path('save',views.saveUrl,name='save'),
    path('form',views.form,name='form'),
    path('access/<slug>',views.erisimFormu,name='erisimFormu'),
    path('success/<slug>',views.success,name='success'),
    path('urlList',views.urlList),
    path('',views.form,name='index'),
    path('<accessed_url>',views.shortenedRedirect)
]