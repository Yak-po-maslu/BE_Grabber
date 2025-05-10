# serializers.py
from rest_framework import serializers
from ads.models import UploadedImageV1

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImageV1
        fields = ['id', 'image', 'uploaded_at']

    def create(self, validated_data):
        instance = UploadedImageV1.objects.create(**validated_data)
        return instance
