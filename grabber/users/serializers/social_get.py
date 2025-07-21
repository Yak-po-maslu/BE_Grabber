from rest_framework import serializers
from ..models import CustomUser, SocialLink


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']