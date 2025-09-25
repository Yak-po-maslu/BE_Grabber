from rest_framework import serializers
from subscriptions.models import NewsletterSubscriber

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[])
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'created_at']
