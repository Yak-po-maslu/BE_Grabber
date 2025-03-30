
from django.urls import path
from grabber_test import views

urlpatterns = [
    path('', views.ping, name='ping'),
]
