
from django.urls import path
from . import views





urlpatterns = [
    path('form',views.form,name='form'),
    path('addUsers/',views.addUsers,name='addUsers'),
    path('access/<slug>',views.erisimFormu,name='erisimFormu'),
    path('success',views.success,name='success'),
    path('htmx/create-user-form/',views.createUserForm,name='create-user-form'),
    path('',views.form,name='index'),
    path('<accessed_url>',views.shortenedRedirect),
    path('deleteUrl/<slug>',views.deleteUrl,name='deleteUrl'),
]