from django.contrib import admin

from ads.models import UploadedImageV1


# Register your models here.
@admin.register(UploadedImageV1)
class UploadedImageAdmin(admin.ModelAdmin):
    model = UploadedImageV1
    list_display = ['id', 'image', 'uploaded_at']