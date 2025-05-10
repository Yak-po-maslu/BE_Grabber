from django.urls import path
from .views import ( index, create_ad, add_image_to_ads, get_moderation,
approve_ad, reject_ad)

urlpatterns = [
    path('', index.index, name='ads_index'),
    path('create-ad/',create_ad.AsyncCreateAdsView.as_view(), name='create-ad'),
    path('<int:ad_id>/add-image/', add_image_to_ads.AddImageToAdsAPIView.as_view(), name='add-image-to-ads'),
    path("moderation/",get_moderation.GetModerationView.as_view(), name='get_moderation'),
    path('approve/<int:ad_id>/', approve_ad.ApproveAdAPIView.as_view(), name='approve-ad'),
    path('reject/<int:ad_id>/', reject_ad.RejectAdAPIView.as_view(), name='reject-ad'),

]
