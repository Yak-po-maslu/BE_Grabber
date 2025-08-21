from rest_framework import serializers
from ads.models import SubCategory

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name", "description", "image", "category"]
        read_only_fields = ["id"]
