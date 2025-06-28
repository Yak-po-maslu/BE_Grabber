# subscriptions/serializers.py

from rest_framework import serializers
from subscriptions.models import NewsletterSubscriber

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'created_at']

    def validate_email(self, value):
        if NewsletterSubscriber.objects.filter(email=value).exists():
            raise serializers.ValidationError("Цей email вже підписаний.")
        return value
