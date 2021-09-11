from django.urls import path
from . import views, auth

urlpatterns = [
    path('travels', views.index),
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),
    path('addtrip', views.addtrip),
    path('view/<id_dest>',views.view),
    path('join/<id_dest>',views.join_travel),
    path('cancel/<id_dest>',views.cancel_travel),
    path('delete/<id_dest>',views.delete_travel),
]
