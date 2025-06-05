from rest_framework import serializers
from ..models import Ad
from django.contrib.auth import get_user_model
User = get_user_model()



class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'phone_number']
class AdSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(source='user', read_only=True)
    class Meta:
        model = Ad
        fields = "__all__"
