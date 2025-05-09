# serializers.py
from rest_framework import serializers
from ..models import UploadedImageV1

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImageV1
        #fields = '__all__'
        fields = ['id', 'image', 'uploaded_at']
