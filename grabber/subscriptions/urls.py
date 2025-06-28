from django.urls import path
from subscriptions.views.subscribe import SubscribeView
from subscriptions.views.get_all_subscribers import GetAllSubscribersAPIView

urlpatterns = [
    path('subscribe/', SubscribeView.as_view(), name='newsletter-subscribe'),
    path('get_subscribers/', GetAllSubscribersAPIView.as_view(), name='get-all-subscribers'),
]