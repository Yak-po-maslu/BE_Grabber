from rest_framework import serializers
from ads.models import Ad

class AddToCartSerializer(serializers.Serializer):
    productId = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_productId(self, value):      
        if not Ad.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value
class RemoveFromCartSerializer(serializers.Serializer):
    productId = serializers.IntegerField()

    def validate_productId(self, value):
        if not Ad.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value