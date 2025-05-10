from django.urls import path
from .views import ( index, upload_image
)

urlpatterns = [
    path('', index.index, name='ads_index'),
    path('upload-image/', upload_image.ImageUploadView.as_view(), name='upload-image'),

]
