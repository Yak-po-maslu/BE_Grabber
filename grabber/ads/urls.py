from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='ads_index'),
    path('upload/', include('ads.upload.urls')),
]
