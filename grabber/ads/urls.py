from django.urls import path
from ads.views.get_ads import AdViewSet
from ads.views.get_main_page import MainPageAdListView
from .views import (
    index,
    create_ad,
    add_image_to_ads,
    get_moderation,
    approve_ad,
    reject_ad,
    delete_ad,
    get_owner_ads
)

urlpatterns = [
    path('', index.index, name='ads_index'),
    path('main-page/', MainPageAdListView.as_view(), name="main-page-ads"),
    path('create/', create_ad.AsyncCreateAdsView.as_view(), name='create-ad'),
    path('<int:ad_id>/add-image/', add_image_to_ads.AddImageToAdsAPIView.as_view(), name='add-image-to-ads'),
    path("moderation/", get_moderation.GetModerationView.as_view(), name='get_moderation'),
    path('<int:ad_id>/approve/', approve_ad.ApproveAdAPIView.as_view(), name='approve-ad'),
    path('<int:ad_id>/reject/', reject_ad.RejectAdAPIView.as_view(), name='reject-ad'),
    path('ads/', AdViewSet.as_view({'get': 'list'}), name='ad-list'),
    path('<int:ad_id>/delete/', delete_ad.DeleteAdView.as_view(), name='delete-ad'),
    path('my/', get_owner_ads.GetAdsAPIView.as_view(), name='owner_ads'),
    
]
