from rest_framework import serializers
from ..views import User


User = User

class UserForgetPassword(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        value = value.strip().lower()
        if not value:
            raise serializers.ValidationError("Email cannot be empty.")
        return value

