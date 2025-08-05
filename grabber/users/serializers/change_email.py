from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class ChangeEmailValidator(serializers.Serializer):
    current_email = serializers.EmailField(required=True)
    new_email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user

        if data['current_email'] != user.email:
            raise serializers.ValidationError({"current_email": "Current email does not match."})

        if not user.check_password(data['password']):
            raise serializers.ValidationError({"password": "Incorrect password."})

        if User.objects.filter(email=data['new_email']).exists():
            raise serializers.ValidationError({"new_email": "This email is already in use."})

        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.email = self.validated_data['new_email']
        user.save()
        return user
