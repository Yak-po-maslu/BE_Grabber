from django.urls import path
from ads.views.update_ad import UpdateAdView
from ads.views.get_main_page import MainPageAdListView
from ads.views.get_ads import AdViewSet
from ads.views.get_recommended_ads import RecommendedAdsAPIView
from .views.add_image_to_category import AddImageToCategoryAPIView
from ads.views.get_faq import FAQListAPIView
from ads.views.delete_category import DeleteCategoryView
from ads.views.favorite import FavoriteAdAddView, FavoriteAdRemoveView, FavoriteAdListView
from ads.views.get_reviews import ProductReviewView
from ads.views.get_product_comments import ProductCommentView
from ads.views.upload_image_view import UploadImageView, DeleteAdImageView
from .views import (
    create_ad,
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
    path('<int:category_id>/upload-image/', AddImageToCategoryAPIView.as_view(), name='upload-category-image'),
    path('categories/<int:category_id>/delete/', DeleteCategoryView.as_view(), name='delete-category'),
    path('<int:ad_id>/', get_one_ad.GetOneAdView.as_view(), name='get-one-ad'),
    path('recommendations/', RecommendedAdsAPIView.as_view(), name='recommended-ads'),
    path('faq/', FAQListAPIView.as_view(), name='faq-list'),
    path('favorites/', FavoriteAdAddView.as_view(), name='add_favorite'),
    path('favorites/<int:product_id>/', FavoriteAdRemoveView.as_view(), name='remove_favorite'),
    path('products/<int:id>/reviews/', ProductReviewView.as_view(), name='product-reviews'),
    path('products/<int:id>/comments/', ProductCommentView.as_view(), name='product-comments'),
    path('upload-image/', UploadImageView.as_view(), name='upload-image'),
    path('images/delete/', DeleteAdImageView.as_view(), name='delete-ad-image'),
    path('favorite/', FavoriteAdListView.as_view(), name='favorite-ads-list'),
    path('products/<int:id>/reviews', ProductReviewView.as_view(), name='product-reviews'),
]
