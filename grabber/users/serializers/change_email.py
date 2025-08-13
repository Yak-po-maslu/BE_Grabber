from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class ChangeEmailValidator(serializers.Serializer):
    current_email = serializers.EmailField(required=True)
    new_email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_current_email(self, value):
        user = self.context['request'].user
        if user.email != value:
            raise serializers.ValidationError("Current email does not match.")
        return value

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect password.")
        return value

    def validate_new_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def save(self):
        user = self.context['request'].user
        user.email = self.validated_data['new_email']
        user.save()
        return user
