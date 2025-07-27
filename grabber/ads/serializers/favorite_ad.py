from rest_framework import serializers
from ads.models import Ad

class FavoriteAdAddSerializer(serializers.Serializer):
    """
    Serializer for adding an Ad to user's favorites.
    """
    product_id = serializers.IntegerField()

class AdListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()  

    class Meta:
        model = Ad
        fields = [
            'id',
            'title',
            'description',
            'price',
            'location',
            'images',
            'status',
            'created_at',
            'category',
            'views',
            'is_recommended',
        ]