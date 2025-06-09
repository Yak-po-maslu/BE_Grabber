from rest_framework import serializers
from ..models import Ad


class AdSerializer(serializers.ModelSerializer):

    category_name = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['id', 'description', 'price', 'user_id',
                  'title', 'status', 'category_name', 'category_id', 'images']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_category_id(self, obj):
        return obj.category.id if obj.category else None
