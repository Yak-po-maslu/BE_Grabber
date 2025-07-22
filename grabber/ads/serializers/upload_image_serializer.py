from rest_framework import serializers
from ads.models import UploadedImageV1

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImageV1
        fields = ['id', 'image', 'uploaded_at']
class DeleteImageSerializer(serializers.Serializer):
    ad_id = serializers.IntegerField()
    image_url = serializers.CharField()