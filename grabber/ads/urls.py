from django.urls import path
from .views import ( index, create_ad, add_image_to_ads
)

urlpatterns = [
    path('', index.index, name='ads_index'),
    path('create-ad/',create_ad.AsyncCreateAdsView.as_view(), name='create-ad'),
    path('<int:ad_id>/add-image/', add_image_to_ads.AddImageToAdsAPIView.as_view(), name='add-image-to-ads'),

]
