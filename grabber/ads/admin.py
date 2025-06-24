from django.contrib import admin
from ads.models import Ad, UploadedImageV1
from .models import FAQ


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'status', 'user', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'category']


@admin.register(UploadedImageV1)
class UploadedImageAdmin(admin.ModelAdmin):
    model = UploadedImageV1
    list_display = ['id', 'image', 'uploaded_at']
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']