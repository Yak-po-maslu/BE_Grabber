from django.urls import path
from ads.views.update_ad import UpdateAdView
from ads.views.get_main_page import MainPageAdListView
from ads.views.get_ads import AdViewSet
from .views import (
    create_ad,
    add_image_to_ads,
    get_moderation,
    approve_ad,
    reject_ad,
    delete_ad,
    get_owner_ads,
    get_categories,
    create_category,
    edit_category,
    get_one_ad
)

urlpatterns = [
    path('', AdViewSet.as_view({'get': 'list'}), name='ad-list'),
    path('main-page/', MainPageAdListView.as_view(), name="main-page-ads"),
    path('create/', create_ad.AsyncCreateAdsView.as_view(), name='create-ad'),
    path('<int:ad_id>/add-image/', add_image_to_ads.AddImageToAdsAPIView.as_view(), name='add-image-to-ads'),
    path("moderation/", get_moderation.GetModerationView.as_view(), name='get_moderation'),
    path('<int:ad_id>/update/', UpdateAdView.as_view(), name='update-ad'),
    path('<int:ad_id>/approve/', approve_ad.ApproveAdAPIView.as_view(), name='approve-ad'),
    path('<int:ad_id>/reject/', reject_ad.RejectAdAPIView.as_view(), name='reject-ad'),
    path('<int:ad_id>/delete/', delete_ad.DeleteAdView.as_view(), name='delete-ad'),
    path('my/', get_owner_ads.GetAdsAPIView.as_view(), name='owner_ads'),
    path('categories/', get_categories.GetCategoriesAPIView.as_view(), name='categories-list'),
    path('categories/create/', create_category.CreateCategoryAPIView.as_view(), name='create-category'),
    path('categories/<int:category_id>/edit/',
         edit_category.EditCategoryAPIView.as_view(), name='edit-category'),
    path('<int:ad_id>/', get_one_ad.GetOneAdView.as_view(), name='get-one-ad'),




]
