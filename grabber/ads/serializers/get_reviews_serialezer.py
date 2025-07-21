from rest_framework import serializers
from ads.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_email', 'rating', 'comment', 'created_at']