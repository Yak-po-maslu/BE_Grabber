from rest_framework import serializers

from ads.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image']
        read_only_fields = ['id']